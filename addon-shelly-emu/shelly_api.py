import math
import logging
from aiohttp import web
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceInfo
import asyncio
import re
import logging
import socket


log = logging.getLogger("shelly_api")

class ShellyEmuAPI:
    def __init__(self, ha_ws, shelly_cfg):
        self.ha = ha_ws
        self.cfg = shelly_cfg
        self.sensors = shelly_cfg.get("sensors", {})
        self.zeroconf = None
        self.mdns_registered = False
        self._initial_pull_event = asyncio.Event()  # Event für Initial-Pull


    async def start_mdns(self):
        """Registriert das Shelly-Gerät via mDNS"""
        if not self.cfg.get("mDNS", True):
            log.info("ℹ️ mDNS deaktiviert (Config).")
            return

        ip_addr = self._get_local_ip()
        if not ip_addr:
            log.warning("⚠️ Lokale IP konnte nicht ermittelt werden, mDNS wird nicht gestartet")
            return

        try:
            ip_bytes = socket.inet_aton(ip_addr)
            self.zeroconf = AsyncZeroconf()
            service_type = "_http._tcp.local."
            name = f"{self.cfg.get('device_name', 'shelly-pro3em-emu')}._http._tcp.local."

            info = AsyncServiceInfo(
                type_=service_type,
                name=name,
                port=self.cfg.get("port", 8080),
                addresses=[ip_bytes],
                properties={
                    "id": self.cfg.get("device_id", "shelly-pro3em-emu-1"),
                    "model": "SHPL-EM3",
                    "fw": "1.0.0-emu"
                }
            )

            await self.zeroconf.async_register_service(info)
            self.mdns_registered = True
            log.info(f"📡 mDNS service registered: {name} ({ip_addr}:{self.cfg.get('port', 8080)})")

        except Exception as e:
            log.warning(f"⚠️ mDNS konnte nicht gestartet werden: {e}")
            self.mdns_registered = False


    async def stop_mdns(self):
        """Beendet den mDNS-Service"""
        try:
            if self.zeroconf and self.mdns_registered:
                await self.zeroconf.async_close()
                log.info("🛑 mDNS service stopped")
        except Exception as e:
            log.warning(f"⚠️ Fehler beim Stoppen von mDNS: {e}")


    def _get_local_ip(self):
        """Ermittelt die lokale IP des Containers automatisch"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            log.warning(f"Fehler beim Ermitteln der lokalen IP: {e}")
            return None


	# ---------------- REST API ----------------
    async def get_status(self, request):
        """Status der emulierten Shelly Pro 3EM"""
        ha = request.app["ha_client"]
        sensors = request.app["sensors"]


        if hasattr(ha, "connected_event"):
            await ha.connected_event.wait()

        def get_value(entity_id):
            if not entity_id:
                return 0.0
            val = ha.cache.get(entity_id)

            try:
                if val in (None, "unknown", "unavailable", ""):
                    log.debug(f"Undefined value for {entity_id}: {val}")
                    return 0.0  # oder None, je nach gewünschtem Verhalten
                return float(val)

            except (ValueError, TypeError):
                log.warning(f"Invalid value for {entity_id}: {val}")
                return 0.0

        emeters = []
        total_power = 0.0

        # for phase_key in ["phase_l1", "phase_l2", "phase_l3"]:
        #     phase_sensors = sensors.get(phase_key, {})
        #     u = get_value(phase_sensors.get("voltage"))
        #     i = get_value(phase_sensors.get("current"))

        #     phi = get_value(phase_sensors.get("phi"))

        #     # --- Phasenwinkel normalisieren (-180° .. +180°) ---
        #     phi = ((phi + 180) % 360) - 180

        #     power_sensor = phase_sensors.get("power")

        #     # Berechne Leistung: P = U * I * cos(phi)
        #     power_calc = u * i * math.cos(math.radians(phi)) if u and i else 0.0

        #     # Wenn Power-Sensor existiert und >0, verwende ihn
        #     power_meas = get_value(power_sensor)
        #     power = power_meas if power_meas > 0 else power_calc

        #     emeters.append({
        #         "voltage": u,
        #         "current": i,
        #         "phi": phi,
        #         "power": round(power, 2)
        #     })
        #     total_power += power

        # Gesamtsummen
        total_cfg = sensors.get("total", {})
        total_power_from_grid_entity = total_cfg.get("power_from_grid")
        total_power_to_grid_entity = total_cfg.get("power_to_grid")
        total_energy_entity = total_cfg.get("energy")

        power_from_grid = get_value(total_power_from_grid_entity) if total_power_from_grid_entity else 0
        power_to_grid = get_value(total_power_to_grid_entity) if total_power_to_grid_entity else 0
        total_power_final = power_from_grid + power_to_grid

        total_energy = get_value(total_energy_entity) if total_energy_entity else 0

        status = {
            "emeters": emeters,
            "total_power": total_power_final,
            "total_energy": total_energy
        }


        p_sum = 0
        for phase_key in ["phase_l1", "phase_l2", "phase_l3"]:
            phase_sensors = sensors.get(phase_key, {})
            u = get_value(phase_sensors.get("voltage"))
            i = get_value(phase_sensors.get("current"))
            p = u * i
            p_sum += p

        corr_factor = total_power_final / p_sum

        for phase_key in ["phase_l1", "phase_l2", "phase_l3"]:
            phase_sensors = sensors.get(phase_key, {})
            u = get_value(phase_sensors.get("voltage"))
            i = get_value(phase_sensors.get("current"))

            # DIRTY HACK: using a correction factor as cos(phi) is unknown when using tibber backend data.
            p = u * i * corr_factor

            emeters.append({
                "voltage": u,
                "current": i,
                "power": p
            })

        # # Gesamtsummen
        # total_cfg = sensors.get("total", {})
        # total_power_entity = total_cfg.get("power")
        # total_energy_entity = total_cfg.get("energy")

        # total_power_final = get_value(total_power_entity) if total_power_entity else round(total_power, 2)
        # total_energy = get_value(total_energy_entity) if total_energy_entity else round(total_power / 1000, 3)






        return web.json_response(status)



    async def get_device_info(self, request):
        return web.json_response({
            "name": self.cfg.get("device_name", "shelly-pro3em-emu"),
            "id": self.cfg.get("device_id", "shelly-pro3em-emu-1"),
            "mac": "AA:BB:CC:DD:EE:01",
            "type": "SHPL-EM3",
            "model": "Shelly Pro 3EM",
            "fw": "1.0.0-emu",
            "ver": "2025-10-09"
        })


def create_app(ha_ws, shelly_cfg):
    api = ShellyEmuAPI(ha_ws, shelly_cfg)
    app = web.Application()

    # CORS Middleware
    @web.middleware
    async def cors_middleware(request, handler):

        resp = await handler(request)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp


    app.middlewares.append(cors_middleware)

    # OPTIONS Handler
    async def handle_options(request):
        return web.Response(headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        })
    app.router.add_route("OPTIONS", "/{tail:.*}", handle_options)

    # REST Endpunkte
    app.router.add_get("/rpc/Shelly.GetStatus", api.get_status)
    app.router.add_get("/rpc/Shelly.GetDeviceInfo", api.get_device_info)

    # Automatisches Mapping der Tibber-Sensoren
    app["ha_client"] = ha_ws
    # app["sensors"] = []
    app["sensors"] = shelly_cfg.get("sensors", {})

    return app, api
