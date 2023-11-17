FROM python:3.10-slim-buster

RUN apt-get update && \
    python -m pip install --upgrade pip && \
    pip install requests prometheus-client

COPY . . 

ENTRYPOINT [ "python", "script.py" ]
