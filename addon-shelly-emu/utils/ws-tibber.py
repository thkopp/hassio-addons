import base64
from websocket import create_connection

user = "admin"
password = "AWK8-B571"
token = base64.b64encode(f"{user}:{password}".encode()).decode()

print("Versuche, WS zu verbinden...")

try:
    ws = create_connection(
        "ws://192.168.40.129/ws",
        header=[f"Authorization: Basic {token}"]
    )
    print("Connected")
except Exception as e:
    print("Fehler bei Verbindung:", e)

while True:
    try:
        msg = ws.recv()
        print("MSG RX:")
        print(msg)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("WS Fehler:", e)
        break
