import logging
import json
import sqlite3
from datetime import datetime

# Configure logging
LOG_FILE = "logging/honeypot.log"
DB_FILE = "logging/honeypot.db"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            service TEXT,
            action TEXT,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Log data in both JSON and database
def log_event(ip, service, action, data):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log to file
    log_entry = {"timestamp": timestamp, "ip": ip, "service": service, "action": action, "data": data}
    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(log_entry) + "\n")
    
    # Log to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, ip, service, action, data) VALUES (?, ?, ?, ?, ?)",
                   (timestamp, ip, service, action, data))
    conn.commit()
    conn.close()

# Initialize the database when the module is imported
init_db()
