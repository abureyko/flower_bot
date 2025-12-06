FROM python:3.12

# Устанавливаем system deps для psycopg2 / asyncpg
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "alembic upgrade head && python -m flower_bot.seed_run && uvicorn flower_bot.main:app --host 0.0.0.0 --port 10000"]
