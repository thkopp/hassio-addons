import asyncio
import logging
import os
import json
from aiohttp import web
from ha_ws import HomeAssistantWS
from shelly_api import create_app

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

CONFIG_PATH = "/data/options.json"

# ---------------- Config Reader ----------------
def load_sensors_from_config(config_path=CONFIG_PATH):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config = json.load(f)

    sensors_cfg = config.get("sensors", {})
    log.info(f"  {sensors_cfg}")

    # Standard-Dict-Struktur, falls Schlüssel fehlen
    sensors = {
        "phase_l1": {"voltage": "", "current": "", "phi": "", "power": ""},
        "phase_l2": {"voltage": "", "current": "", "phi": "", "power": ""},
        "phase_l3": {"voltage": "", "current": "", "phi": "", "power": ""},
        "total": {"power": "", "energy": ""}
    }

    # Update vorhandene Werte
    for key in sensors.keys():
        if key in sensors_cfg:
            sensors[key].update(sensors_cfg[key])

    # Logging
    log.info("✅ Sensoren aus Config geladen:")
#    for phase, values in sensors.items():
#        log.info(f"  {phase}: {values}")

    return sensors

def flatten_sensor_entities(sensors):
    """Alle gültigen Entity-IDs in eine flache Liste"""
    entities = []
    for phase in ["phase_l1", "phase_l2", "phase_l3", "total"]:
        entities.extend([v for v in sensors.get(phase, {}).values() if v])
    return entities

# ---------------- Main Server ----------------
async def start_servers():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    ha_cfg = config.get("ha_connect", {})
    shelly_cfg = config.get("shelly_pro3em", {})
    sensors = load_sensors_from_config()
    entities = flatten_sensor_entities(sensors)

    # Home Assistant WS Client
    ha_ws = HomeAssistantWS(
        ha_url=ha_cfg.get("ha_url"),
        token=ha_cfg.get("ha_token"),
        entities=entities
    )

    # WS-Client starten
    asyncio.create_task(ha_ws.connect())
    await ha_ws.connected_event.wait()
    log.info(f"✅ Initialwerte von Home Assistant sind geladen, Cache Keys: {list(ha_ws.cache.keys())}")

    # ---------------- Shelly API ----------------
    rpc_app, api = create_app(ha_ws, shelly_cfg)
    rpc_app["ha_client"] = ha_ws
    rpc_app["sensors"] = sensors

    # mDNS starten (falls aktiviert)
    asyncio.create_task(api.start_mdns())

    # RPC Server starten
    port = int(shelly_cfg.get("port", 1010))
    rpc_runner = web.AppRunner(rpc_app)
    await rpc_runner.setup()
    rpc_site = web.TCPSite(rpc_runner, host="0.0.0.0", port=port)
    await rpc_site.start()
    log.info(f"✅ Shelly Emulator läuft auf Port {port}")

    # Dashboard starten (Ingress)
    WEB_DIR = "/app/web"
    dash_app = web.Application()
    dash_app.router.add_static('/static', WEB_DIR, show_index=True)

    async def index(request):
        return web.FileResponse(os.path.join(WEB_DIR, 'index.html'))

    dash_app.router.add_get('/', index)
    dash_runner = web.AppRunner(dash_app)
    await dash_runner.setup()
    dash_site = web.TCPSite(dash_runner, host="0.0.0.0", port=8080)
    await dash_site.start()
    log.info(f"✅ Dashboard läuft (Ingress-kompatibel) auf Port 8080")

    # Endlosschleife
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        log.info("🛑 Beende Shelly Emulator...")
    finally:
        await ha_ws.close()
        await rpc_runner.cleanup()
        await dash_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(start_servers())
