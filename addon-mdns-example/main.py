#!/usr/bin/env python3
import time
import json
import socket
from zeroconf import ServiceInfo, Zeroconf
from pathlib import Path

# Standardwerte
DEVICE_NAME = "mdns-test-addon"
PORT = 8080

# Optionen aus HA UI lesen
options_file = Path("/data/options.json")
if options_file.exists():
    try:
        with open(options_file) as f:
            options = json.load(f)
            DEVICE_NAME = options.get("device_name", DEVICE_NAME)
            PORT = int(options.get("port", PORT))
    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von options.json: {e}")

# Lokale IP ermitteln
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

ip_addr = get_local_ip()
ip_bytes = socket.inet_aton(ip_addr)

desc = {"info": "Minimal mDNS Test Addon"}

info = ServiceInfo(
    "_http._tcp.local.",
    f"{DEVICE_NAME}._http._tcp.local.",
    addresses=[ip_bytes],
    port=PORT,
    properties=desc,
    server=f"{DEVICE_NAME}.local.",
)

zeroconf = Zeroconf()
try:
    zeroconf.register_service(info)
    print(f"📡 mDNS Service registered: {DEVICE_NAME} on {ip_addr}:{PORT}")
    print("⏳ Press Ctrl+C to exit...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Shutting down mDNS...")
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()
