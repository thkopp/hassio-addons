#!/usr/bin/with-contenv bashio
# Shelly Emulator Start-Skript für mDNS Test Addon

set -e

bashio::log.info "ℹ️ Starte mDNS Test Addon..."

# Environment-Variablen aus Addon-Konfiguration
export DEVICE_NAME=$(bashio::config 'device_name')
export PORT=$(bashio::config 'port')

# Python Skript starten
python3 /app/main.py
