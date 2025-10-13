#!/usr/bin/env bash
# run.sh – Minimal mDNS Test Addon

set -e

DEVICE_NAME="${DEVICE_NAME:-mdns-test-addon}"
PORT="${PORT:-8080}"

echo "ℹ️ Starte mDNS Service für $DEVICE_NAME auf Port $PORT..."

# Starte Python-Skript, das mDNS registriert
python3 main.py "$DEVICE_NAME" "$PORT"
