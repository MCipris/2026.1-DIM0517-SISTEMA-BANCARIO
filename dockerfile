FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

COPY . /app/

RUN python 2026.1-DIM9517-SISTEMA-BANCARIO/banco_Safe/manage.py collectstatic --noinput || true

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "2026.1-DIM9517-SISTEMA-BANCARIO.banco_Safe.banco_Safe.wsgi:application"]