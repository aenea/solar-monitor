FROM python:3-slim-bullseye

COPY startup.sh /scripts/startup.sh
COPY solar-monitor.py /scripts/solar-monitor.py

RUN pip install --upgrade pip && \
    pip install --no-cache-dir paho-mqtt && \
    pip install --no-cache-dir renogymodbus && \
    rm -rf /root/.cache/pip && \
    mkdir -p /scripts && \
    chmod +x /scripts/startup.sh

ENTRYPOINT [ "/bin/bash", "-c", "/scripts/startup.sh" ]