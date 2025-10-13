#!/usr/bin/env python3
"""
Minimal MDNS Test Addon
Registriert einen HTTP-Service via Zeroconf
"""

import asyncio
import logging
import socket
from zeroconf import ServiceInfo, Zeroconf

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mdns-test")

SERVICE_TYPE = "_http._tcp.local."
SERVICE_NAME = "mdns-test-addon._http._tcp.local."
SERVICE_PORT = 8080

def get_local_ip():
    """Ermittelt die lokale IP des Containers"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        log.warning(f"Fehler beim Ermitteln der IP: {e}")
        return "127.0.0.1"

async def main():
    zeroconf = Zeroconf()
    ip_addr = socket.inet_aton(get_local_ip())

    info = ServiceInfo(
        type_=SERVICE_TYPE,
        name=SERVICE_NAME,
        addresses=[ip_addr],
        port=SERVICE_PORT,
        properties={"version": "0.0.1"},
        server="mdns-test.local."
    )

    try:
        zeroconf.register_service(info)
        log.info(f"📡 mDNS Service registriert: {SERVICE_NAME} ({get_local_ip()}:{SERVICE_PORT})")
        # keep running
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        log.info("🛑 Stoppe mDNS Service")
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()

if __name__ == "__main__":
    asyncio.run(main())
