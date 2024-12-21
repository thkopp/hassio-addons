#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start the MiniDLNA daemon
# s6-overlay docs: https://github.com/just-containers/s6-overlay
# ==============================================================================

set -e

CONFIG="/etc/minidlna.conf"
bashio::log.info "Creating MiniDLNA configuration ${CONFIG}"

# Declare variables
declare port
declare media_dir
declare album_art_names
declare inotify
declare enable_tivo
declare tivo_discovery
declare strict_dlna
declare notify_interval
declare serial
declare model_number


{
  echo "port=$(bashio::config 'port')"
  echo "media_dir=$(bashio::config 'media_dir')"
  echo "album_art_names=$(bashio::config 'album_art_names')"
  echo "inotify=$(bashio::config 'inotify')"
  echo "enable_tivo=$(bashio::config 'enable_tivo')"
  echo "tivo_discovery=$(bashio::config 'tivo_discovery')"
  echo "strict_dlna=$(bashio::config 'strict_dlna')"
  echo "notify_interval=$(bashio::config 'notify_interval')"
  echo "serial=$(bashio::config 'serial')"
  echo "model_number=$(bashio::config 'model_number')"
  echo "=$(bashio::config '')"
} > "${CONFIG}"

bashio::log.info "Starting MiniDLNA service"
exec minidlnad  
#| ts '[%Y-%m-%d %H:%M:%S]'

