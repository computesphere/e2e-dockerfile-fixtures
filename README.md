# e2e Dockerfile fixtures

Tiny Dockerfiles that ComputeSphere's end-to-end checks build from git:

- `no-cmd/`: a Python image with no `CMD` of its own. Started with a start command, it serves on `$PORT`; without one it runs the base image's command.
- `with-cmd/`: the same image with a `CMD` that serves on `$PORT`.
- `entrypoint/`: an `ENTRYPOINT` wrapper that prints a line, then runs its `CMD`.

Each serves `index.html` naming its directory, so a request shows which one answered.
