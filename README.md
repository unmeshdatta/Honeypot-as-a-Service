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

## Contributions
Feel free to contribute by adding new honeypot services, improving logging, or enhancing the dashboard.

## License
MIT License
