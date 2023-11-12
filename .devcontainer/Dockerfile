FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

RUN apt update \
    && apt install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD [ "bin/bash" ]