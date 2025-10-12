import asyncio
import socket
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceBrowser
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("shelly_test")

class ShellyListener:
    def __init__(self):
        self.found = []

    def remove_service(self, zeroconf, type_, name):
        log.info(f"Service removed: {name}")

    def add_service(self, zeroconf, type_, name):
        log.info(f"Service found: {name}")
        self.found.append(name)


async def main():
    azc = AsyncZeroconf()
    listener = ShellyListener()
    service_type = "_http._tcp.local."
    browser = AsyncServiceBrowser(azc.zeroconf, service_type, listener)

    # Warte ein paar Sekunden auf mDNS-Responses
    await asyncio.sleep(5)

    if listener.found:
        log.info(f"Gefundene Shelly-Emus: {listener.found}")
        # Test: GetStatus von erstem gefundenen Gerät abrufen
        first = listener.found[0]
        info = azc.zeroconf.get_service_info(service_type, first)
        if info:
            ip = socket.inet_ntoa(info.addresses[0])
            port = info.port
            url = f"http://{ip}:{port}/rpc/Shelly.GetStatus"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    log.info(f"GetStatus Response: {data}")
    else:
        log.warning("Keine Shelly-Emus im LAN gefunden!")

    await azc.async_close()


if __name__ == "__main__":
    asyncio.run(main())
