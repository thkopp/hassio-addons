import asyncio
import socket
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceInfo
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mdns_test")

async def main():
    name = "test-mdns-device._http._tcp.local."
    port = 8080
    ip = socket.gethostbyname(socket.gethostname())
    log.info(f"📡 Registering mDNS service {name} on {ip}:{port}")

    zc = AsyncZeroconf()
    info = AsyncServiceInfo(
        type_="_http._tcp.local.",
        name=name,
        port=port,
        addresses=[socket.inet_aton(ip)],
        properties={"version": "1.0"},
    )
    await zc.async_register_service(info)

    try:
        log.info("✅ mDNS Service running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await zc.async_unregister_service(info)
        await zc.async_close()
        log.info("🛑 mDNS Service stopped.")

if __name__ == "__main__":
    asyncio.run(main())
