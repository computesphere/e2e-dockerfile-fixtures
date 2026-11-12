# e2e Dockerfile fixtures

Tiny Dockerfiles that ComputeSphere's end-to-end checks build from git:

- `no-cmd/`: a Python image with no `CMD` of its own. Started with a start command, it serves on `$PORT`; without one it runs the base image's command.
- `with-cmd/`: the same image with a `CMD` that serves on `$PORT`.
- `entrypoint/`: an `ENTRYPOINT` wrapper that prints a line, then runs its `CMD`.
- `syntax-official/`: `with-cmd/` with the parser directive `# syntax=docker/dockerfile:1`, the official Dockerfile frontend.
- `django-celery-redis/`: a one-file Django app with a Celery worker in the same container, both on `REDIS_URL`. `/redis` pings through redis-py; `/celery` runs one task through the broker and the result backend. With a `rediss://` URL ending in `?ssl_cert_reqs=required&ssl_ca_certs=<CA file>`, both verify the cache's certificate.
- `syntax-custom/`: `with-cmd/` with a parser directive naming a frontend image at an `.invalid` host. A build that only allows the official frontend refuses it.

Each serves `index.html` naming its directory, so a request shows which one answered.
