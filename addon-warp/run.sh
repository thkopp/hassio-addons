#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start the WARP daemon
# s6-overlay docs: https://github.com/just-containers/s6-overlay
# ==============================================================================

set -e

CONFIG="/etc/wake-on-arp.conf"
bashio::log.info "Creating WARP configuration ${CONFIG}"

# Declare variables
declare WARP_IP_ADDRESS
declare WOL_MAC_ADDRESS
declare NETWORK_INTERFACE
declare BROADCAST_IP
declare SUBNET_MASK
declare ALLOW_GATEWAY

# Create main config
WARP_IP_ADDRESS=$(bashio::config 'warp_ip_address')
WOL_MAC_ADDRESS=$(bashio::config 'wol_mac_address')
NETWORK_INTERFACE=$(bashio::config 'network_interface')
BROADCAST_IP=$(bashio::config 'broadcast_ip')
SUBNET_MASK=$(bashio::config 'subnet_mask')
ALLOW_GATEWAY=$(bashio::config 'allow_gateway')

if [ $(bashio::config 'allow_gateway') = "true" ]; then
  ALLOW_GATEWAY="-ag"
else
  ALLOW_GATEWAY=""
fi;

{
  echo "# Target IP and MAC address pairs"
  echo "target_ip_1 ${WARP_IP_ADDRESS}"
  echo "target_mac_1 ${WOL_MAC_ADDRESS}"
  echo
  echo "# Network device to scan on"
  echo "net_device ${NETWORK_INTERFACE}"
  echo
  echo "# Broadcast IP address"
  echo "broadcast_ip ${BROADCAST_IP}"
  echo
  echo "# Net mask that describes which source IP's are allowed"
  echo "subnet ${SUBNET_MASK}"
  echo
  echo "# Allow wake on arp requests from the gateway"
  echo "${ALLOW_GATEWAY}"
  echo
  echo "# Ignores ARP requests from this IP (you can add as many of these as you like)"
  echo "source_exclude 192.168.1.5"
} > "${CONFIG}"

# mycmd=(wake-on-arp -i ${WARP_IP_ADDRESS} -m ${WOL_MAC_ADDRESS} -d ${NETWORK_INTERFACE} -b ${BROADCAST_IP} -s ${SUBNET_MASK} ${ALLOW_GATEWAY})
mycmd=wake-on-arp

bashio::log.info "Creating list of network clients"
echo
awk 'BEGIN {printf("%19s | %18s | %16s | %s\n", "Network Interface", "MAC Address", "IP Address", "Network Client")}'
echo "--------------------+--------------------+------------------+------------------"
arp | tr -d {}[]\(\) | awk '!/incomplete/ && !/hassio/ && !/docker0/ {printf("%19s | %18s | %16s | %s\n", $7, $4, $2, $1)}'
echo
bashio::log.info "Starting ${mycmd[@]} service"
exec ${mycmd[@]}