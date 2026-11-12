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
# Fail fast: a broker that can't be reached or verified answers within seconds, not after retries.
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_connection_timeout=5,
    broker_connection_max_retries=1,
    task_publish_retry=False,
    redis_socket_connect_timeout=5,
    redis_socket_timeout=10,
    result_expires=300,
)


@celery_app.task(name="app.add")
def add(a, b):
    return a + b


def reason(e):
    """The failure class only: never the URL, host or password."""
    parts, seen = [], set()
    while e is not None and id(e) not in seen:  # Celery wraps the cause: read the whole chain
        seen.add(id(e))
        parts.append(f"{type(e).__name__} {e}")
        e = e.__cause__ or e.__context__
    text = " ".join(parts).lower()
    for needle, why in (
        ("certificate_verify_failed", "certificate_verify_failed"),
        ("certificate verify failed", "certificate_verify_failed"),
        ("no such file", "ca_file_not_found"),
        ("ssl_ca_certs", "ca_file_not_found"),
        ("wrongpass", "auth"),
        ("noauth", "auth"),
        ("authentication", "auth"),
        ("name or service not known", "dns"),
        ("nodename nor servname", "dns"),
        ("timed out", "timeout"),
        ("timeout", "timeout"),
        ("connection refused", "refused"),
    ):
        if needle in text:
            return why
    return "other"


def fail(e):
    return JsonResponse({"ok": False, "error_class": type(e).__name__, "reason": reason(e)}, status=503)


def index(_request):
    return JsonResponse({"ok": True, "app": "django-celery-redis"})


def redis_ping(_request):
    try:
        return JsonResponse({"ok": bool(redis.Redis.from_url(REDIS_URL, socket_connect_timeout=5, socket_timeout=10).ping())})
    except Exception as e:  # the failure class is the point of this fixture
        return fail(e)


def celery_roundtrip(_request):
    try:
        return JsonResponse({"ok": True, "result": add.delay(2, 3).get(timeout=30)})
    except Exception as e:
        return fail(e)


urlpatterns = [path("", index), path("redis", redis_ping), path("celery", celery_roundtrip)]
application = get_wsgi_application()

if not REDIS_URL:
    print("REDIS_URL is not set: /redis and /celery will fail", file=sys.stderr, flush=True)
