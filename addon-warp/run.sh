#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start the WARP daemon
# s6-overlay docs: https://github.com/just-containers/s6-overlay
# ==============================================================================

set -e

CONFIG="/etc/wake-on-arp.conf"
bashio::log.info "Creating WARP configuration ${CONFIG}"

# Declare variables
declare NETWORK_INTERFACE
declare BROADCAST_IP
declare SUBNET_MASK
declare ALLOW_GATEWAY

# Create main config
NETWORK_INTERFACE=$(bashio::config 'network_interface')
BROADCAST_IP=$(bashio::config 'broadcast_ip')
SUBNET_MASK=$(bashio::config 'subnet_mask')
ALLOW_GATEWAY=$(bashio::config 'allow_gateway')

{
  echo "# Target IP and MAC address pairs"
  echo "target_ip_1          $(bashio::config 'target_ip_1')"
  echo "target_mac_1         $(bashio::config 'target_mac_1')"
  echo
  echo "# Network device to scan on"
  echo "net_device           ${NETWORK_INTERFACE}"
  echo
  echo "# Broadcast IP address"
  echo "broadcast_ip         ${BROADCAST_IP}"
  echo
  echo "# Net mask that describes which source IP's are allowed"
  echo "subnet               ${SUBNET_MASK}"
  echo
  echo "# Allow wake on arp requests from the gateway"
  echo "allow_gateway        ${ALLOW_GATEWAY}"
  echo
  echo "# Ignores ARP requests from this IP (you can add as many of these as you like)"
  echo "source_exclude 192.168.1.5"
} > "${CONFIG}"


bashio::log.info "Creating list of network clients"
bashio::log.green "$(printf '\t+----------------+--------------------+------------------+--------------------------------+\n')"
bashio::log.green "$(awk 'BEGIN {printf("\t| %-14s | %-18s | %-16s | %-30s |\n", "INTERFACE", "MAC ADDRESS", "IP ADDRESS", "HOSTNAME")}')"
bashio::log.green "$(printf '\t+----------------+--------------------+------------------+--------------------------------+\n')"
bashio::log.green "$(arp | tr -d '{}[]\(\)' | awk '!/incomplete/ && !/hassio/ && !/docker0/ {printf("\t| %-14s | %-18s | %-16s | %-30s |\n", $7, $4, $2, substr($1,1,30))}')"
bashio::log.green "$(printf '\t+----------------+--------------------+------------------+--------------------------------+\n')"
bashio::log.info "Starting wake-on-arp service"
exec wake-on-arp | ts '[%Y-%m-%d %H:%M:%S]'

