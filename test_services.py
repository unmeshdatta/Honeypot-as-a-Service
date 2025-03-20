import unittest
import os
import sqlite3
from logging.logger import log_event, init_db
from threat_intelligence.api_integration import check_abuseipdb, check_shodan

class TestLogging(unittest.TestCase):
    def setUp(self):
        self.db_file = "logging/honeypot_test.db"
        self.log_file = "logging/honeypot_test.log"
        os.environ["DB_FILE"] = self.db_file  # Override database file for testing

        # Initialize test database
        init_db()

    def test_log_event(self):
        log_event("192.168.1.1", "SSH", "Login Attempt", "User: admin")
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs")
        logs = cursor.fetchall()
        conn.close()
        self.assertGreater(len(logs), 0)

class TestThreatIntelligence(unittest.TestCase):
    def test_check_abuseipdb(self):
        response = check_abuseipdb("8.8.8.8")  # Testing with Google Public DNS IP
        self.assertIsNotNone(response)

    def test_check_shodan(self):
        response = check_shodan("8.8.8.8")
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()
