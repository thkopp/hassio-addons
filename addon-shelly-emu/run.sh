#!/usr/bin/with-contenv bashio

bashio::log.info "Starte Shelly Pro 3EM Emulator..."

exec python3 /app/main.py
