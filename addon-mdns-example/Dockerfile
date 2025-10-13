ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.5
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip && \
    pip install zeroconf

COPY run.sh /app/run.sh
COPY main.py /app/main.py
RUN chmod +x /app/run.sh

CMD [ "/app/run.sh" ]
