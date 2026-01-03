ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.23
FROM ${BUILD_FROM}

WORKDIR /app

RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-aiohttp \
    py3-websockets \
    py3-zeroconf

COPY main.py ha_ws.py shelly_api.py /app/
COPY web/ /app/web

# Service-Startskript für s6
COPY run.sh /usr/bin/run.sh
RUN chmod +x /usr/bin/run.sh

EXPOSE 80

# Kein CMD / ENTRYPOINT!
# s6 (/init) übernimmt den Start
