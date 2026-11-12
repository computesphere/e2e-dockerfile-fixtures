#!/bin/sh
# One container: the Celery worker in the background, the web app in the foreground on $PORT.
set -e
celery -A app:celery_app worker --loglevel=info --concurrency=1 &
exec gunicorn app:application --bind "0.0.0.0:${PORT:-8000}" --workers 2 --access-logfile -
