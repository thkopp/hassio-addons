import sys
import asyncio
import socket
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceInfo
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mdns_test")

async def main(name, port):
    azc = AsyncZeroconf()

    # Lokale IP bestimmen
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    service_type = "_http._tcp.local."
    service_name = f"{name}.{service_type}"
    desc = {"info": "mDNS Test Addon via Zeroconf"}

    info = AsyncServiceInfo(
        service_type,
        service_name,
        addresses=[socket.inet_aton(ip)],
        port=port,
        properties=desc,
        server=f"{name}.local."
    )

    await azc.async_register_service(info)
    log.info(f"✅ mDNS-Dienst registriert: {service_name} ({ip}:{port})")

    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        log.info("🛑 Beende mDNS-Test...")
        await azc.async_unregister_service(info)
        await azc.async_close()

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "shelly-mdns-test"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    asyncio.run(main(name, port))
