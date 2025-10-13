#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "Starte mDNS Test Add-on..."
python3 /app/main.py
