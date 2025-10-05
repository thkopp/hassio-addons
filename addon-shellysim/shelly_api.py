# shelly_api.py
from aiohttp import web
import logging
from zeroconf import ServiceInfo, Zeroconf
import socket

_LOG = logging.getLogger("shelly_api")

def _is_on(raw_state):
    if raw_state is None:
        return False
    s = str(raw_state).lower()
    return s in ("on", "true", "1", "open")

class ShellyServer:
    def __init__(self, ha_client, mappings, device_name="shelly-emu", port=8080):
        self.ha_client = ha_client
        self.mappings = mappings
        self.device_name = device_name
        self.port = port
        self.zeroconf = None

    async def handle_status(self, request):
        relays = []
        for rid, ent in self.mappings["relays"].items():
            st = self.ha_client.state_store.get(ent, {})
            relays.append({"id": int(rid), "ison": _is_on(st.get("state"))})

        sensors = {}
        for name, ent in self.mappings["sensors"].items():
            st = self.ha_client.state_store.get(ent, {})
            sensors[name] = st.get("state")

        return web.json_response({
            "id": self.mappings["device_id"],
            "name": "Shelly-Emu",
            "relays": relays,
            "sensors": sensors
        })

    async def handle_relay(self, request):
        relay_id = request.match_info.get("relay_id")
        query = request.rel_url.query

        if "turn" not in query:
            ent = self.mappings["relays"].get(relay_id)
            if not ent:
                return web.Response(status=404, text="Relay not mapped")
            current = self.ha_client.state_store.get(ent, {}).get("state")
            return web.json_response({"ison": _is_on(current)})

        turn = query.get("turn", "").lower()
        ent = self.mappings["relays"].get(relay_id)
        if not ent:
            return web.Response(status=404, text="Relay not mapped")

        domain = ent.split(".", 1)[0]
        service = "turn_on" if turn in ("on", "1", "true") else "turn_off"
        await self.ha_client.call_service(domain, service, {"entity_id": ent})

        return web.json_response({"result": "ok"})

    async def start_http(self):
        app = web.Application()
        app.add_routes([
            web.get("/status", self.handle_status),
            web.get("/relay/{relay_id}", self.handle_relay),
        ])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        _LOG.info("HTTP server running on port %s", self.port)

    def start_mdns(self):
        self.zeroconf = Zeroconf()
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        info = ServiceInfo(
            type_="_http._tcp.local.",
            name=f"{self.device_name}._http._tcp.local.",
            addresses=[socket.inet_aton(ip)],
            port=self.port,
            properties={},
            server=f"{self.device_name}.local.",
        )
        self.zeroconf.register_service(info)
        _LOG.info("mDNS advertised as %s.local:%s", self.device_name, self.port)
