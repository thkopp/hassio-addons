# Home Assistant Add-on: WARP

WARP - Wake on ARP<br>
An ARP based wake on LAN server

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield] [![license][gplv3-shield]](license.MD)

This add-on provides a Wake-on-ARP server for your network. It listens for ARP requests to trigger Wake-on-LAN Magic packets.<br>
<br>
In this first version, this addon builds the Wake-on-ARP binary from source code during installation. This installation process could damage your micro SD card if you are using a small device like a Raspberry Pi.<br>
<br>
After installation you can check the startup logs for a mapping bewteen IP adresses and MAC addresses. This list of network clients will only show devices answering to an arp request on your main network interface. If the device is visible in the list you can use its IP address and MAC address for the configuration. <br>

```
[22:40:59] INFO: Creating list of network clients...
[22:40:59] INFO:
[22:40:59] INFO:   Network Interface |        MAC Address |       IP Address | Network Client
[22:40:59] INFO: --------------------+--------------------+------------------+------------------
[22:41:02] INFO:                eth0 |  b7:40:e1:98:d0:95 |      192.168.0.9 | NAS-server
```

Based on [wake-on-arp](https://github.com/nikp123/wake-on-arp)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[gplv3-shield]: https://img.shields.io/badge/license-GPLv3-blue
