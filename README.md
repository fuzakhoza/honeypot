# Autonomous Intrusion Prevention System (IPS) & Honeypot

## 🎯 Objective
This project simulates an inline **Intrusion Prevention System (IPS)** and a **Network Honeypot**. It sits actively on a system's network interface adapter, intercepts unauthorized reconnaissance traffic (such as ping sweeps or Nmap port scans), extracts threat intelligence, and executes an automated firewall block dynamically.

## ⚙️ How It Works (The Security Logic)
1. **Network Interface Binding:** The script binds natively to port `8080` across all interfaces (`0.0.0.0`), intercepting traffic at the network card boundary.
2. **Traffic Interception:** Before a packet can traverse into internal server directories, the script catches the socket connection and extracts the attacker's Source IP and Source Port.
3. **Threat Intelligence Parsing:** The tool contacts a geo-IP registry to determine the physical location and ISP of the attacker, while inspecting packet payload headers for automated testing signatures (e.g., Nmap footprints).
4. **Active Remediation:** If a signature matches or unauthorized access is attempted, the IP is instantly appended to a dynamic `FIREWALL_BLOCKLIST`. Subsequent connection drops are handled automatically.

## 🧪 Real-World Simulation Test
This tool was actively verified using a dual-machine lab infrastructure:
*   **Target Machine (Windows 10 Workstation):** Hosting the automated Python IPS application engine.
*   **Attacking Machine (Kali Linux Laptop):** Initiated an active reconnaissance probe using the command:  
    `nmap -p 8080 [Target_IP]`

### 🚨 Live Execution Output Captured:
```text
📡 [IPS ACTIVE] Monitoring organization traffic on Port 8080...
🛡️ Ready to intercept, analyze, and block suspicious reconnaissance drops...

🚨 [ALERT] Inbound connection detected at 2026-05-17 15:15:22!
👉 Source IP: 192.168.43.210 | Source Port: 43214
🔍 Extracting attacker intelligence...
📍 Attacker Location: Localhost (Internal Attack Simulation)
⚙️ Service/Tool Fingerprint (sV): Nmap Reconnaissance Scan Signature Detected
⚡ [ACTION TAKEN] Adding 192.168.43.210 to the dynamic Firewall Blocklist.
🔒 Status: 192.168.43.210 is now blocked from reaching internal server infrastructure.
```

## 🛠️ Environment & Dependencies
*   **OS:** Windows 10 & Kali Linux Interoperability
*   **Language:** Python 3.x (Standard Socket & Sys Modules)
*   **Libraries:** `requests` (For remote geographic IP parsing API updates)
