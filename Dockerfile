FROM python:3.12-slim-bookworm

ENV DB_HOST=212.113.123.161 \
    DB_USERNAME=gen_user \
    DB_PASSWORD=efim_admin \
    DB_PORT=5432 \
    DB_NAME=default_db \
    APP_HOST=217.25.89.163

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "./mini_app_server.py"]