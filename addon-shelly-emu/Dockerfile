ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /app

# Installiere Python + benötigte Pakete nur mit apk (kein pip nötig!)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-aiohttp \
    py3-websockets \
    py3-zeroconf

# Dateien ins Image kopieren
COPY main.py ha_ws.py shelly_api.py /app/
COPY run.sh /app/

# Dashboard kopieren
COPY web/ /app/web

# run.sh ausführbar machen
RUN chmod a+x /app/run.sh

EXPOSE 8080 1010 5353

# Start
CMD [ "/app/run.sh" ]
