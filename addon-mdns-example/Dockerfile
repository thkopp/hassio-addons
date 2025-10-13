FROM python:3-alpine

# Arbeitsverzeichnis
WORKDIR /app

# Python-Abhängigkeiten
RUN python3 -m pip install zeroconf --root-user-action=ignore

# Addon-Dateien kopieren
COPY main.py config.yaml ./

# Ports
EXPOSE 8080/tcp 5353/udp

# Startbefehl
CMD ["python3", "-u", "main.py"]
