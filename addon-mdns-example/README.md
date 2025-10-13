# 🧠 Home Assistant Add-on: mDNS Test

Ein kleines Add-on, das einen `_http._tcp` mDNS-Dienst broadcastet.
Ideal, um mDNS-Discovery in Home Assistant oder im Netzwerk zu testen.

### 🔧 Optionen

| Name        | Typ    | Beschreibung            | Default              |
| ----------- | ------ | ----------------------- | -------------------- |
| `mdns_name` | string | Anzeigename im Netzwerk | `"test-mdns-device"` |
| `mdns_port` | int    | TCP-Port                | `8080`               |

### 🚀 Installation

1. Repository in Home Assistant hinzufügen:
