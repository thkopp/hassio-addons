#!/usr/bin/with-contenv bashio
# Shelly Emulator Start-Skript

bashio::log.info "Starte Shelly Emulator..."

# Home Assistant URL und Token aus Add-on-Umgebungsvariablen
#export HA_URL="http://supervisor/core"
#export HA_TOKEN=$(bashio::config 'ha_token')

# Python-Skript starten
python3 /app/main.py