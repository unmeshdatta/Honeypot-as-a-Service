# Honeypot-as-a-Service (HAAS)

## Overview

This project is a deployable Honeypot system designed to detect and log unauthorized access attempts.

## Features

- **SSH & FTP Honeypots** to lure attackers
- **Logs attacker IPs and actions in SQLite & JSON**
- **Threat Intelligence Integration (AbuseIPDB, VirusTotal, Shodan)**
- **Web Dashboard for attack monitoring (Planned)**
- **Docker-based deployment for easy setup**

---

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/Honeypot-as-a-Service.git
cd Honeypot-as-a-Service
```

### 2. Install Dependencies
Ensure you have Python 3 installed, then run:
```sh
pip install -r requirements.txt
```

---

## Running the Honeypots

### Start the SSH Honeypot:
```sh
python honeypot_services/ssh_honeypot.py
```

### Start the FTP Honeypot:
```sh
python honeypot_services/ftp_honeypot.py
```

### View Logs:
Logs are stored in `logging/honeypot.log` and the SQLite database (`logging/honeypot.db`).
```sh
cat logging/honeypot.log
sqlite3 logging/honeypot.db "SELECT * FROM logs;"
```

---

## Deployment using Docker

### Build the Docker Image:
```sh
docker build -t honeypot .
```

### Run the Honeypot in a Container:
```sh
docker run -p 22:22 -p 21:21 -p 5000:5000 honeypot
```

This will expose:
- **Port 22** for SSH Honeypot
- **Port 21** for FTP Honeypot
- **Port 5000** (Future Web Dashboard)

---

## Source Code

### `honeypot_services/ssh_honeypot.py` (SSH Honeypot)
```python
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
```

### `honeypot_services/ftp_honeypot.py` (FTP Honeypot)
```python
from twisted.protocols.ftp import FTPFactory, FTPRealm, FTP
from twisted.cred.portal import Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
import logging

# Configure logging
logging.basicConfig(filename="logging/honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class FakeFTPUser(FTP):
    def ftp_USER(self, username):
        logging.info(f"FTP Login Attempt - Username: {username}")
        return FTP.ftp_USER(self, username)

    def ftp_PASS(self, password):
        logging.info(f"FTP Password Attempt - Password: {password}")
        return FTP.ftp_PASS(self, password)

    def ftp_LIST(self, path):
        logging.info(f"FTP LIST Command Executed - Path: {path}")
        return FTP.ftp_LIST(self, path)

    def ftp_RETR(self, filename):
        logging.info(f"FTP File Download Attempt - Filename: {filename}")
        return FTP.ftp_RETR(self, filename)

    def ftp_STOR(self, filename):
        logging.info(f"FTP File Upload Attempt - Filename: {filename}")
        return FTP.ftp_STOR(self, filename)

# Setting up the FTP Honeypot
def start_ftp_honeypot():
    realm = FTPRealm()
    portal = Portal(realm, [InMemoryUsernamePasswordDatabaseDontUse(anonymous="anonymous")])
    factory = FTPFactory(portal)
    factory.protocol = FakeFTPUser

    logging.info("Starting FTP Honeypot on port 21")
    reactor.listenTCP(21, factory)
    reactor.run()

if __name__ == "__main__":
    start_ftp_honeypot()
```

---

## Contributions
Feel free to contribute by adding new honeypot services, improving logging, or enhancing the dashboard.

## License
MIT License
