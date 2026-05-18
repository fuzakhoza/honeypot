

import socket
import sys
import json
import requests
from datetime import datetime

# A list to simulate our active firewall blocklist
FIREWALL_BLOCKLIST = []

def get_ip_location(ip_address):
    """Fetches geolocation metadata for the attacking IP address."""
    # Using a free, public IP lookup API for the demonstration
    if ip_address == "127.0.0.1":
        return "Localhost (Internal Attack Simulation)"
    try:
        response = requests.get(f"https://ipapi.co{ip_address}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            country = data.get("country_name", "Unknown Country")
            city = data.get("city", "Unknown City")
            isp = data.get("org", "Unknown ISP")
            return f"{city}, {country} (ISP: {isp})"
    except Exception:
        pass
    return "Unknown Location (API Timeout)"

def run_ips_honeypot(port=80):
    """Listens for incoming packets, extracts metadata, and triggers a firewall block."""
    # Set up a TCP socket to listen for incoming reconnaissance/connection attempts
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        print(f"📡 [IPS ACTIVE] Monitoring organization traffic on Port {port}...")
        print("🛡️ Ready to intercept, analyze, and block suspicious reconnaissance drops...\n")
    except Exception as e:
        print(f"⚠️ Failed to bind to port {port}: {e}")
        sys.exit(1)

    try:
        while True:
            # Intercept incoming connection attempt before it reaches any real server files
            client_socket, client_address = server_socket.accept()
            attacker_ip = client_address[0]
            attacker_port = client_address[1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"🚨 [ALERT] Inbound connection detected at {timestamp}!")
            print(f"👉 Source IP: {attacker_ip} | Source Port: {attacker_port}")

            # 1. DEFENSIVE INTERCEPTION: Check if IP is already blocked
            if attacker_ip in FIREWALL_BLOCKLIST:
                print(f"🛑 [FIREWALL DROPPED] Request from {attacker_ip} blocked automatically. Terminating connection.\n")
                client_socket.close()
                continue

            # 2. INTELLIGENCE GATHERING: Fetch Attacker Location
            print("🔍 Extracting attacker intelligence...")
            location = get_ip_location(attacker_ip)
            print(f"📍 Attacker Location: {location}")

            # 3. SERVICE VERSION DETECTION SIMULATION (sV Analysis)
            # Read the raw packet payload to analyze the tool or signature the hacker used
            try:
                payload = client_socket.recv(1024).decode('utf-8', errors='ignore')
                if "Nmap" in payload or not payload:
                    service_version_guess = "Nmap Reconnaissance Scan Signature Detected"
                else:
                    service_version_guess = f"Custom Tool Payload Signature: User-Agent Profile Detected"
                print(f"⚙️ Service/Tool Fingerprint (sV): {service_version_guess}")
            except Exception:
                print("⚙️ Service/Tool Fingerprint (sV): Stealth Connection Drop (No Payload)")

            # 4. ACTIVE REMEDIATION: Put the IP on the firewall blocklist
            print(f"⚡ [ACTION TAKEN] Adding {attacker_ip} to the dynamic Firewall Blocklist.")
            FIREWALL_BLOCKLIST.append(attacker_ip)
            print(f"🔒 Status: {attacker_ip} is now blocked from reaching internal server infrastructure.\n")
            print("-" * 80 + "\n")

            # Terminate and isolate the attacker
            client_socket.close()

    except KeyboardInterrupt:
        print("\nStopping IPS Engine safely. Clearing active dynamic firewall configurations.")
        server_socket.close()

if __name__ == "__main__":
    # Simulating the engine on standard Web Port 80
    run_ips_honeypot(port=80)
