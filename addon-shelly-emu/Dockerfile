ARG BUILD_FROM
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

# COPY run.sh /
# RUN chmod a+x /run.sh

EXPOSE 80

# CMD [ "/run.sh" ]