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
