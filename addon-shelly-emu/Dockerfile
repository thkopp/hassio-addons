ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM ${BUILD_FROM}

WORKDIR /app

RUN apk add --no-cache python3 py3-pip py3-aiohttp py3-websockets py3-zeroconf

COPY main.py ha_ws.py shelly_api.py /app/
COPY run.sh /app/
COPY web/ /app/web
RUN chmod +x /app/run.sh

EXPOSE 80

