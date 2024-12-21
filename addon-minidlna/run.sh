#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start the MiniDLNA daemon
# s6-overlay docs: https://github.com/just-containers/s6-overlay
# ==============================================================================

set -e

CONFIG="/etc/minidlna.conf"
bashio::log.info "Creating MiniDLNA configuration ${CONFIG}"

# Declare variables
declare media_dir
declare inotify


# Create main config
media_dir_A=$(bashio::config 'A,/media/music')                   
inotify=$(bashio::config 'no')                                   # 'no' for less resources, restart required for new media

{
  echo "media_dir=$(bashio::config 'media_dir_A')"
  echo "inotify=$(bashio::config 'inotify')"
} >> "${CONFIG}"


bashio::log.info "Starting MiniDLNA service"
exec minidlnad  | ts '[%Y-%m-%d %H:%M:%S]'

