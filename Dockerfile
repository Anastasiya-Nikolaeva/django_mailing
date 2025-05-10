FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTHECODE=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --no-input && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]

