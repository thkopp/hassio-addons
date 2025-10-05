import asyncio
import logging
import os
import json

from ha_ws import HAClient
from shelly_api import ShellyServer

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger("main")

# Add-on Optionen werden von Home Assistant in /data/options.json gespeichert
OPTIONS_FILE = "/data/options.json"

def load_options():
    if not os.path.exists(OPTIONS_FILE):
        _LOG.error("Options file not found: %s", OPTIONS_FILE)
        return {}
    with open(OPTIONS_FILE, "r") as f:
        opts = json.load(f)

    # Relays und Sensors aus Listen ("key:value") in Dicts umwandeln
    relays = {}
    for entry in opts.get("relays", []):
        try:
            k, v = entry.split(":", 1)
            relays[k.strip()] = v.strip()
        except ValueError:
            _LOG.warning("Invalid relay entry: %s", entry)

    sensors = {}
    for entry in opts.get("sensors", []):
        try:
            k, v = entry.split(":", 1)
            sensors[k.strip()] = v.strip()
        except ValueError:
            _LOG.warning("Invalid sensor entry: %s", entry)

    mappings = {
        "device_id": opts.get("device_id", "shelly-emu-1"),
        "relays": relays,
        "sensors": sensors
    }

    return {
        "device_name": opts.get("device_name", "shelly-emu"),
        "port": int(opts.get("port", 8080)),
        "mDNS": opts.get("mDNS", True),
        "coap": opts.get("coap", False),
        "mappings": mappings
    }

async def main():
    opts = load_options()

    ha_url = os.environ.get("HA_URL", "http://homeassistant:8123")
    ha_token = os.environ.get("HA_TOKEN", "")

    if not ha_token:
        _LOG.error("No HA_TOKEN provided! Create a long-lived token in Home Assistant.")
        return

    ha_client = HAClient(ha_url, ha_token)
    shelly = ShellyServer(
        ha_client,
        opts["mappings"],
        device_name=opts["device_name"],
        port=opts["port"]
    )

    if opts["mDNS"]:
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
