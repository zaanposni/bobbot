FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY main.py .
COPY config.json .

ENTRYPOINT [ "python", "-u", "main.py" ]
