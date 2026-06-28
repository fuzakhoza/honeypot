import socket
import json

def run_security_console(port=9999):
    """Listens for network broadcast alerts from the IPS honeypot."""
    console_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    console_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to port 9999 to listen for the incoming Wi-Fi broadcasts
    console_socket.bind(('0.0.0.0', port))
    print(f"🖥️ [SECURITY CONSOLE LISTENING] Awaiting network threat telemetry on port {port}...\n")

    try:
        while True:
            data, address = console_socket.recvfrom(4096)
            try:
                # Parse the incoming thief alert data string back into a readable dictionary
                alert = json.loads(data.decode('utf-8'))
                
                print("=" * 50)
                print(f"💥 WARNING: [{alert['EVENT']}] ALARM TRIGGERED BY WORKSTATION!")
                print(f"📅 Time of Incident: {alert['TIMESTAMP']}")
                print(f"🥷 Attacker IP:      {alert['ATTACKER_IP']}")
                print(f"🔍 Tool Signature:   {alert['SIGNATURE']}")
                print(f"📍 Physical Origin:  {alert['LOCATION']}")
                print(f"🛡️ Action Enforced:  {alert['STATUS']}")
                print("=" * 50 + "\n")
                
            except Exception as e:
                print(f"Received malformed broadcast payload: {e}")
                
    except KeyboardInterrupt:
        print("\nShutting down Security Management Console.")
        console_socket.close()

if __name__ == "__main__":
    run_security_console(port=9999)
