# Shelly Emulator Add-on für Home Assistant

Dieses Add-on simuliert ein **Shelly-Gerät** im lokalen Netzwerk und stellt Home Assistant-Sensordaten sowie Schalter so dar, als kämen sie von einem echten Shelly.
Damit können andere Geräte im LAN (z. B. Smart-Home-Gateways oder Apps) die simulierten Shellys wie Original-Hardware erkennen.

---

## ✨ Features

- Stellt Home Assistant-Entities als **Shelly-kompatible Relays und Sensoren** dar
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
relays:
  - "0:switch.kitchen_socket"
  - "1:switch.livingroom_socket"
sensors:
  - "temperature:sensor.livingroom_temperature"
  - "humidity:sensor.livingroom_humidity"
ha_token: "DEIN_LONG_LIVED_ACCESS_TOKEN"
```
