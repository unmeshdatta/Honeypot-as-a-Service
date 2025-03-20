import requests
import json

# API Keys (replace with actual keys)
ABUSEIPDB_API_KEY = "YOUR_ABUSEIPDB_API_KEY"
VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY"
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"

# Function to check IP reputation using AbuseIPDB
def check_abuseipdb(ip):
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

# Function to check file reputation using VirusTotal
def check_virustotal(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

# Function to get IP information using Shodan
def check_shodan(ip):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    test_ip = "8.8.8.8"  # Example IP for testing
    print("AbuseIPDB:", check_abuseipdb(test_ip))
    print("Shodan:", check_shodan(test_ip))
