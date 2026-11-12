#!/bin/sh
# One container: the Celery worker in the background, the web app in the foreground on $PORT.
# The worker restarts when it exits (a cache not reachable yet at start), so /celery recovers.
set -e
(while :; do celery -A app:celery_app worker --loglevel=info --concurrency=1 || true; echo "celery worker exited; restarting in 5 s" >&2; sleep 5; done) &
exec gunicorn app:application --bind "0.0.0.0:${PORT:-8000}" --workers 2 --access-logfile -
