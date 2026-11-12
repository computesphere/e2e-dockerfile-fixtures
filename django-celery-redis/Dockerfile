# Built from the repository root (docker build -f django-celery-redis/Dockerfile .), as a monorepo's
# Dockerfile usually is.
FROM python:3.12-slim
WORKDIR /app
COPY django-celery-redis/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY django-celery-redis/app.py django-celery-redis/start.sh ./
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["./start.sh"]
