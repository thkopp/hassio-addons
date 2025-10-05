# Basis-Image von Home Assistant Add-ons
# ARG BUILD_FROM=ghcr.io/hassio-addons/base:14.3.2
ARG BUILD_FROM
FROM ${BUILD_FROM}

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten installieren
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-aiohttp \
    py3-websockets \
    py3-zeroconf \
    && pip3 install --no-cache-dir aiohttp websockets zeroconf

# Python-Skripte ins Image kopieren
COPY main.py ha_ws.py shelly_api.py /app/
COPY run.sh /app/

# Startskript ausführbar machen
RUN chmod a+x /app/run.sh

# Container Start
CMD [ "/app/run.sh" ]
