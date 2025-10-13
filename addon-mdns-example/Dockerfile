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
        && adduser -D -h /app app

WORKDIR /app

RUN python3 -m pip install zeroconf --root-user-action=ignore

COPY run.sh main.py config.yaml ./

USER app

EXPOSE 8080/tcp 5353/udp

ENTRYPOINT ["/sbin/tini", "-s", "--"]
CMD ["bash", "run.sh"]