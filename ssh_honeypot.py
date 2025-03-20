import paramiko
import socket
import threading
import logging

# Configure logging
logging.basicConfig(filename="logging/honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Fake credentials to allow attackers in
FAKE_CREDENTIALS = [("root", "root"), ("admin", "password"), ("user", "1234")]

class SSHHoneypot(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        logging.info(f"Login attempt - Username: {username}, Password: {password}")
        if (username, password) in FAKE_CREDENTIALS:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "password"

def start_honeypot(host="0.0.0.0", port=22):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f"SSH Honeypot listening on {host}:{port}")

    while True:
        client, addr = server_socket.accept()
        logging.info(f"Connection attempt from {addr}")
        transport = paramiko.Transport(client)
        transport.add_server_key(paramiko.RSAKey.generate(2048))
        server = SSHHoneypot()
        try:
            transport.start_server(server=server)
            channel = transport.accept(20)
            if channel:
                channel.send("Fake SSH Shell. Type 'exit' to quit.\n")
                while True:
                    command = channel.recv(1024).decode("utf-8").strip()
                    if command.lower() == "exit":
                        break
                    logging.info(f"Command executed: {command}")
                    channel.send(f"Command '{command}' not found.\n")
                channel.close()
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            transport.close()

if __name__ == "__main__":
    start_honeypot()
