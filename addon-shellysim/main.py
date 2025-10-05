# main.py
# Startet Add-on, startet HTTP Server, WebSocket Listener und mDNS/CoAP Threads

import asyncio
import logging
import os
from ha_ws import HAClient
from shelly_api import ShellyServer

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger("main")

# Konfiguration: HA_URL, Token und Mappings
HA_URL = os.environ.get("HA_URL", "http://homeassistant:8123")
HA_TOKEN = os.environ.get("HA_TOKEN", "")
MAPPINGS = {
    "device_id": "shelly-emulator-1",
    "relays": {"0": "switch.kitchen_socket"},
    "sensors": {"temperature": "sensor.livingroom_temperature"}
}

async def main():
    ha_client = HAClient(HA_URL, HA_TOKEN)
    shelly = ShellyServer(ha_client, MAPPINGS)
    shelly.start_mdns()
    await asyncio.gather(
        ha_client.run_ws(),
        shelly.start_http()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _LOG.info("Exiting Shelly Emulator")
