# Shelly Emulator Add-on für Home Assistant

Dieses Add-on emuliert einen **Shelly Pro 3EM** Energie- und Leitsungsmesser im lokalen Netzwerk und stellt Home Assistant-Sensordaten so dar, als kämen sie von einem echten Shelly. Es exponiert eine REST-API und mDNS für die LAN-Integration.

Shelly Pro 3EM: https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen2/ShellyProEM

Damit können andere Geräte im LAN (z. B. Smart-Home-Gateways oder Apps) das simulierten Shelly wie Original-Hardware erkennen.

---

## ✨ Features

- Stellt Home Assistant-Entities als **Shelly-Sensoren** dar
- **HTTP API** (`/status`, `/relay/{id}`) wie bei echten Shelly-Geräten
- Optional **mDNS** (Zeroconf) zur Discovery im LAN
- Zukünftig auch **CoAP** Unterstützung möglich
- Läuft als eigenständiges Add-on in Home Assistant OS/Supervised

---

## ⚙️ Konfiguration

Die Konfiguration erfolgt über die Add-on-Optionen (`config.yaml`).
Beispiel:

```yaml
device_name: "shelly-emu"
port: "8080"
mDNS: "true"
coap: "false"
device_id: "shelly-emulator-1"
sensors:
  - "temperature:sensor.livingroom_temperature"
  - "humidity:sensor.livingroom_humidity"
ha_token: "DEIN_LONG_LIVED_ACCESS_TOKEN"
```
