ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.14-alpine3.23
FROM ${BUILD_FROM}

WORKDIR /app

RUN apk add --no-cache \
    py3-pip \
    py3-aiohttp \
    py3-websockets \
    py3-zeroconf

COPY rootfs /
COPY main.py ha_ws.py shelly_api.py /app/
COPY web/ /app/web

EXPOSE 80
