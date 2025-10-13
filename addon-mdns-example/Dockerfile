FROM python:3.12-alpine

# Metadata
LABEL maintainer="thkopp" \
      description="Minimal mdns test addon" \
      version="0.0.1"

# Optional: User setzen, Host-Avahi nutzt Root nicht
USER app

# Systempakete inkl. py3-zeroconf
RUN apk add --no-cache \
        bash \
        dbus \
        avahi \
        avahi-tools \
        py3-zeroconf \
        socat \
        tini \
        curl \
        iproute2 \
        && adduser -D -h /app app

# Arbeitsverzeichnis
WORKDIR /app
USER app

# Copy Addon Files
COPY run.sh main.py config.yaml ./

# Expose Ports
EXPOSE 8080/tcp 5353/udp

# Entrypoint
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["bash", "run.sh"]
