#!/usr/bin/env bash
# ------------------------------
# run.sh - mDNS Test Addon
# ------------------------------
set -e

echo "ℹ️ Starte mDNS Test Addon..."

# Optional: DBus + Avahi (wenn Host-Avahi nicht genutzt wird)
# apk add py3-dbus avahi avahi-tools bereits im Dockerfile
if command -v dbus-daemon >/dev/null 2>&1; then
    echo "ℹ️ Starte DBus-Daemon..."
    dbus-daemon --system &
fi

if command -v avahi-daemon >/dev/null 2>&1; then
    echo "ℹ️ Starte Avahi-Daemon..."
    avahi-daemon --no-chroot &
fi

# Python Skript starten
echo "ℹ️ Starte Python mDNS Service..."
python3 /app/main.py
