ARG BUILD_FROM_AMD64
ARG BUILD_FROM_ARM64

ARG TARGETARCH
FROM ${TARGETARCH} ? ghcr.io/home-assistant/amd64-base:3.23 : ghcr.io/home-assistant/aarch64-base:3.23

WORKDIR /app

RUN apk add --no-cache python3 py3-pip py3-aiohttp py3-websockets py3-zeroconf

COPY main.py ha_ws.py shelly_api.py /app/
COPY run.sh /app/
COPY web/ /app/web
RUN chmod +x /app/run.sh

EXPOSE 80
CMD [ "/app/run.sh" ]
