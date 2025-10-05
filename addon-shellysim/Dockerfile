FROM python:3.11-slim
WORKDIR /app
COPY main.py /app/main.py
RUN pip install aiohttp websockets zeroconf
EXPOSE 8080
CMD ["python", "main.py"]
