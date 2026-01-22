FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# libpq-dev is often needed for psycopg2 (if used) or other db drivers
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Command is overridden by docker-compose, but good to have a default
CMD ["uvicorn", "app.main:app", "host", "0.0.0.0", "port", "8000"]
