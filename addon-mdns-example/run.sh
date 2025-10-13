#!/usr/bin/with-contenv bashio
# Starte mDNS-Test

set -e
bashio::log.info "Starte mDNS-Testdienst..."

SERVICE_NAME=$(bashio::config 'service_name')
PORT=$(bashio::config 'port')

python3 /app/main.py "$SERVICE_NAME" "$PORT"
