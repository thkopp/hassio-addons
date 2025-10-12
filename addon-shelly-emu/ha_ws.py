import asyncio
import json
import logging
import aiohttp
from collections import OrderedDict

log = logging.getLogger("ha_ws")

MAX_CACHE_SIZE = 100  # Optional: max. Anzahl Entities im Cache

class HomeAssistantWS:
    def __init__(self, ha_url: str, token: str, entities: list[str]):
        self.ha_url = ha_url.rstrip("/")
        self.token = token
        self.ws_url = self.ha_url.replace("http", "ws") + "/api/websocket"
        self.session = None
        self.ws = None
        self.msg_id = 0
        self.lock = asyncio.Lock()
        self.cache = OrderedDict()
        self.entities = entities
        self._response_futures = {}
        self.connected_event = asyncio.Event()
        self._stop_event = asyncio.Event()
        self.listener_task = None

    async def connect(self):
        while not self._stop_event.is_set():
            try:
                await self._run_connection()
                log.info("WebSocket-Verbindung beendet, warte 5s vor reconnect")
                await asyncio.sleep(5)
            except Exception as e:
                log.error(f"WebSocket error, reconnecting in 5s: {e}")
                await asyncio.sleep(5)

    async def _run_connection(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

        log.info(f"Connecting to HA WebSocket at {self.ws_url}")
        self.ws = await self.session.ws_connect(self.ws_url, heartbeat=30)

        hello = await self.ws.receive_json()
        if hello.get("type") != "auth_required":
            raise RuntimeError(f"Unexpected hello: {hello}")

        await self.ws.send_json({"type": "auth", "access_token": self.token})
        auth_resp = await self.ws.receive_json()
        if auth_resp.get("type") != "auth_ok":
            raise RuntimeError(f"Auth failed: {auth_resp}")
        log.info("✅ Authentifiziert mit Home Assistant WebSocket")

        self.listener_task = asyncio.create_task(self._ws_listener())
        await asyncio.sleep(0.5)

        await self._initial_pull()
        self.connected_event.set()
        await self._subscribe_state_changes()

        await self.listener_task

    async def _ws_listener(self):
        try:
            async for msg in self.ws:
                if msg.type != aiohttp.WSMsgType.TEXT:
                    continue
                data = json.loads(msg.data)

                if "id" in data and data["id"] in self._response_futures:
                    fut = self._response_futures.pop(data["id"])
                    if not fut.done():
                        fut.set_result(data)
                    continue

                if data.get("type") == "event":
                    event = data.get("event", {})
                    entity_id = event.get("data", {}).get("entity_id")
                    new_state = event.get("data", {}).get("new_state", {}).get("state")
                    if entity_id in self.entities:
                        self.cache[entity_id] = str(new_state)
                        if len(self.cache) > MAX_CACHE_SIZE:
                            self.cache.popitem(last=False)
                        log.debug(f"🔄 Updated {entity_id} = {new_state}")
        except Exception as e:
            log.error(f"Listener Exception: {e}")
        finally:
            if not self._stop_event.is_set():
                log.warning("WebSocket Listener beendet, Verbindung wird neu aufgebaut")

    async def _send_request(self, payload, timeout=10):
        async with self.lock:
            self.msg_id += 1
            req_id = self.msg_id
            payload["id"] = req_id
            fut = asyncio.get_event_loop().create_future()
            self._response_futures[req_id] = fut
            await self.ws.send_json(payload)
            try:
                return await asyncio.wait_for(fut, timeout=timeout)
            finally:
                self._response_futures.pop(req_id, None)

    async def _initial_pull(self):
        log.info("⏳ Starte Initial-Pull der Home Assistant States...")

        try:
            resp = await asyncio.wait_for(
                self._send_request({"type": "get_states"}), timeout=10.0
            )
        except asyncio.TimeoutError:
            log.warning("⏱ Timeout beim Abrufen aller States")
            for entity_id in self.entities:
                self.cache[entity_id] = None
            return

        if resp.get("type") != "result" or not resp.get("success", False):
            log.warning(f"⚠️ HA WebSocket get_states failed: {resp}")
            for entity_id in self.entities:
                self.cache[entity_id] = None
            return

        log.info(f"get_states response keys: {list(resp.keys())}, len(result)={len(resp.get('result', []))}")


        result = resp.get("result", [])
        for entity_id in self.entities:
            val = None
            for item in result:
                if item.get("entity_id") == entity_id:
                    val = item.get("state")
                    break
            self.cache[entity_id] = str(val) if val is not None else None
            if len(self.cache) > MAX_CACHE_SIZE:
                self.cache.popitem(last=False)
            log.debug(f"📩 Initial state {entity_id} = {val}")

        log.info("✅ Initialwerte von Home Assistant sind geladen")

    async def _subscribe_state_changes(self):
        await self._send_request({
            "type": "subscribe_events",
            "event_type": "state_changed"
        })
        log.info("📡 Subscribed to state_changed events")

    async def get_state(self, entity_id: str):
        return self.cache.get(entity_id)

    async def close(self):
        self._stop_event.set()
        if self.listener_task:
            self.listener_task.cancel()
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
