from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Function to fetch logs from database
def fetch_logs():
    conn = sqlite3.connect("logging/honeypot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, ip, service, action, data FROM logs ORDER BY timestamp DESC LIMIT 50")
    logs = cursor.fetchall()
    conn.close()
    return logs

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logs")
def logs():
    data = fetch_logs()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
