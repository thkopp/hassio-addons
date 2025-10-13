#!/usr/bin/env python3
import sys
import time
from zeroconf import ServiceInfo, Zeroconf
import socket

device_name = sys.argv[1] if len(sys.argv) > 1 else "mdns-test-addon"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

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

desc = {'info': 'Minimal mDNS Test Addon'}

info = ServiceInfo(
    "_http._tcp.local.",
    f"{device_name}._http._tcp.local.",
    addresses=[ip_bytes],
    port=port,
    properties=desc,
    server=f"{device_name}.local."
)

zeroconf = Zeroconf()
try:
    zeroconf.register_service(info)
    print(f"📡 mDNS Service registered: {device_name} on {ip_addr}:{port}")
    print("⏳ Press Ctrl+C to exit...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Shutting down mDNS...")
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()
