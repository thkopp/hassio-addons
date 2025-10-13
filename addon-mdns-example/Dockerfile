FROM python:3.12-alpine

# Metadata
LABEL maintainer="thkopp" \
      description="Minimal mDNS test addon" \
      version="0.0.1"

# Systempakete + Python pip
RUN apk add --no-cache \
        bash \
        dbus \
        avahi \
        avahi-tools \
        socat \
        tini \
        curl \
        iproute2 \
        && python3 -m ensurepip \
        && python3 -m pip install --upgrade pip \
        && python3 -m pip install zeroconf \
        && adduser -D -h /app app

# Arbeitsverzeichnis
WORKDIR /app
USER app

# Copy Addon Files
COPY run.sh main.py config.yaml ./

# Expose Ports
EXPOSE 8080/tcp 5353/udp

# Entrypoint mit Tini als PID 1
ENTRYPOINT ["/sbin/tini", "-s", "--"]
CMD ["python3", "run.sh"]
