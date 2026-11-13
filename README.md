# e2e Dockerfile fixtures

Tiny Dockerfiles that ComputeSphere's end-to-end checks build from git:

- `no-cmd/`: a Python image with no `CMD` of its own. Started with a start command, it serves on `$PORT`; without one it runs the base image's command.
- `with-cmd/`: the same image with a `CMD` that serves on `$PORT`.
- `context-copy/`: a Dockerfile that copies a file from its own folder, so it builds only with that folder as the build context, not the repository root.
- `entrypoint/`: an `ENTRYPOINT` wrapper that prints a line, then runs its `CMD`.
- `syntax-official/`: `with-cmd/` with the parser directive `# syntax=docker/dockerfile:1`, the official Dockerfile frontend.
- `django-celery-redis/`: a one-file Django app with a Celery worker in the same container, both on `REDIS_URL`, built from the repository root. `/redis` pings through redis-py; `/celery` runs one task through the broker and the result backend. With a `rediss://` URL ending in `?ssl_cert_reqs=required&ssl_ca_certs=<CA file>`, both verify the cache's certificate.
- `syntax-custom/`: `with-cmd/` with a parser directive naming a frontend image at an `.invalid` host. A build that only allows the official frontend refuses it.
- `multi-stage/`: a two-stage build; the final image copies `index.html` from the first stage.
- `build-secret/`: reads the build secret `FIXTURE_SECRET` with `RUN --mount=type=secret` and prints only its size. Without that secret the build fails.
- `socket-probe/`: a `RUN` step that fails the build if it can see a BuildKit daemon socket directory through `/proc`; it prints the count first. The build argument `PROBE_NONCE` keeps the step from being cached.
- `userns-probe/`: a `RUN` step that prints the user namespace mappings it runs under (`/proc/self/uid_map`, and pid 1's uid and gid maps), and fails the build if it can write a host-wide kernel setting (`/proc/sys/kernel/core_pattern`; it writes back the value it read, so nothing changes). The build argument `PROBE_NONCE` keeps the step from being cached.

Each serves `index.html` naming its directory, so a request shows which one answered.

Base images are pinned by digest, so a moved tag is a reviewed change.
