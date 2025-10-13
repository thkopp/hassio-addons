#!/usr/bin/env bash
# run.sh
DEVICE_NAME="${DEVICE_NAME:-mdns-test-addon}"
PORT="${PORT:-8080}"

echo "ℹ️ Starte mDNS Service für $DEVICE_NAME auf Port $PORT..."

python3 main.py "$DEVICE_NAME" "$PORT"
