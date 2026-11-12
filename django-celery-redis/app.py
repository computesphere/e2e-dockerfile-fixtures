"""A one-file Django app with a Celery worker, both on REDIS_URL.

The cache's rediss:// URL verifies with the environment's CA when REDIS_URL ends in
?ssl_cert_reqs=required&ssl_ca_certs=<ca file>: redis-py and Celery read it from the URL.

GET /         "ok"
GET /redis    redis-py PING through REDIS_URL
GET /celery   one task through the Celery broker and result backend (both REDIS_URL)
"""
import os
import sys

import django
from django.conf import settings
from django.http import JsonResponse

settings.configure(
    DEBUG=False,
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF=__name__,
    SECRET_KEY=os.environ.get("SECRET_KEY", "fixture-only-not-a-secret"),
    MIDDLEWARE=[],
    INSTALLED_APPS=[],
)
django.setup()

import redis  # noqa: E402
from celery import Celery  # noqa: E402
from django.core.wsgi import get_wsgi_application  # noqa: E402
from django.urls import path  # noqa: E402

REDIS_URL = os.environ.get("REDIS_URL", "")
celery_app = Celery("app", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(broker_connection_retry_on_startup=True, result_expires=300)


@celery_app.task(name="app.add")
def add(a, b):
    return a + b


def index(_request):
    return JsonResponse({"ok": True, "app": "django-celery-redis"})


def redis_ping(_request):
    try:
        return JsonResponse({"ok": bool(redis.Redis.from_url(REDIS_URL).ping())})
    except Exception as e:  # the reason is the point of this fixture
        return JsonResponse({"ok": False, "error": f"{type(e).__name__}: {e}"}, status=503)


def celery_roundtrip(_request):
    try:
        return JsonResponse({"ok": True, "result": add.delay(2, 3).get(timeout=30)})
    except Exception as e:
        return JsonResponse({"ok": False, "error": f"{type(e).__name__}: {e}"}, status=503)


urlpatterns = [path("", index), path("redis", redis_ping), path("celery", celery_roundtrip)]
application = get_wsgi_application()

if not REDIS_URL:
    print("REDIS_URL is not set: /redis and /celery will fail", file=sys.stderr, flush=True)
