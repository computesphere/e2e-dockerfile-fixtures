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
- `userns-probe/`: a `RUN` step that prints the user namespace mappings it runs under (`/proc/self/uid_map`, and pid 1's uid and gid maps), and fails the build if it can write a host-wide kernel setting (`/proc/sys/kernel/core_pattern`; it writes back the value it read and prints it before and after, so nothing changes). A deliberate escape probe: run it only in a development build environment. The build argument `PROBE_NONCE` keeps the step from being cached.
- `seccomp-log-probe/`: one `RUN` step in which `python3` makes two system calls, each exactly once: it opens and closes a netlink route socket, which BuildKit's default profile for build steps allows (the known positive for an outer profile that logs the socket families it doesn't allow), and it calls `uselib(NULL)` (x86_64 number 134), which that default profile refuses with EPERM, so no outer profile sees it (the known negative). Neither call does anything lasting, and the build passes whatever they return. A second step prints the kernel's Yama `ptrace_scope` as a build step reads it. The build argument `PROBE_NONCE` keeps the step from being cached.
- `seccomp-step-probe/`: one `RUN` step, written as a heredoc, in which `python3` tries `unshare(CLONE_NEWUSER)` and a tmpfs `mount` and fails the build unless each is refused with EPERM, then reports `chroot("/")` and one HTTPS GET to pypi.org. Nothing changes on the host. The build argument `PROBE_NONCE` keeps the step from being cached.
- `seccomp-i386-probe/`: writes a 93-byte 32-bit x86 program that only calls `exit(0)` through `int 0x80`, runs it once and prints its exit status. Under a seccomp profile that lists only x86_64 it is killed (`exit status 159`, SIGSYS). The step always passes. The build argument `PROBE_NONCE` keeps the step from being cached.
- `build-canary/`: a small build that copies `index.html` and runs one step, then serves the file on `$PORT` with BusyBox `httpd`. The build argument `CANARY_NONCE` keeps the step from being cached. Built every few minutes to check that builds work.
- `build-canary-broken/`: the failing twin of `build-canary/`: its `RUN` step exits 1, so every build of it fails. Used to prove a failed build is reported.
- `failure-modes/`: a Go web service that fails in a chosen way, set by `MODE`: `ok` answers 200 everywhere; `oom` allocates memory on `GET /burst` until the container runs out of it; `oom-start` does the same at startup, before it listens, so every start runs out of memory; `reset` closes every connection but `/healthz` with a TCP reset; `refuse` listens on nothing but `/healthz` on `HEALTH_PORT` (default 8081), so a deploy that checks `PORT` finds nothing there. `wrong-port` serves on `WRONG_PORT` (default 8081) and never on `PORT`, like an app that binds its own port; `loopback` serves on `PORT` but only on `127.0.0.1`. Every mode that serves logs `listening on <address>` at startup. It listens on `PORT` (default 8080), with no secrets, no outbound calls and no storage. Builds from its own folder, either with its `Dockerfile` or as a Go app.

Each serves `index.html` naming its directory, so a request shows which one answered.

Base images are pinned by digest, so a moved tag is a reviewed change.
