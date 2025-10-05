# ha_ws.py
# Modul für Home Assistant WebSocket / REST Kommunikation (lesen von Sensoren, Steuerung von Relays)
import asyncio
import json
import logging
import aiohttp
import websockets

_LOG = logging.getLogger("ha_ws")

class HAClient:
    def __init__(self, ha_url, token):
        self.ha_url = ha_url
        self.token = token
        self.ws_url = ha_url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
        self.state_store = {}

    async def call_service(self, domain, service, data):
        url = f"{self.ha_url}/api/services/{domain}/{service}"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                _LOG.info("Called HA service %s.%s -> %s", domain, service, resp.status)
                return resp.status

    async def run_ws(self):
        while True:
            try:
                _LOG.info("Connecting to HA WebSocket at %s", self.ws_url)
                async with websockets.connect(self.ws_url) as ws:
                    msg = json.loads(await ws.recv())
                    if msg.get("type") == "auth_required":
                        await ws.send(json.dumps({"type": "auth", "access_token": self.token}))
                        auth_resp = json.loads(await ws.recv())
                        if auth_resp.get("type") != "auth_ok":
                            raise RuntimeError(f"Auth failed: {auth_resp}")
                        _LOG.info("Authenticated to HA WebSocket")

                    await ws.send(json.dumps({"id": 1, "type": "get_states"}))
                    await ws.send(json.dumps({"id": 2, "type": "subscribe_events", "event_type": "state_changed"}))

                    while True:
                        raw = await ws.recv()
                        msg = json.loads(raw)
                        if msg.get("type") == "result" and msg.get("id") == 1:
                            for s in msg.get("result", []):
                                eid = s.get("entity_id")
                                if eid:
                                    self.state_store[eid] = {"state": s.get("state"), "attributes": s.get("attributes", {})}
                        if msg.get("type") == "event":
                            event = msg.get("event")
                            if event.get("event_type") == "state_changed":
                                data = event.get("data", {})
                                entity = data.get("entity_id")
                                new_state = data.get("new_state")
                                if entity and new_state:
                                    self.state_store[entity] = {
                                        "state": new_state.get("state"),
                                        "attributes": new_state.get("attributes", {}),
                                    }
            except Exception as e:
                _LOG.exception("WebSocket error (reconnecting in 5s): %s", e)
                await asyncio.sleep(5)
