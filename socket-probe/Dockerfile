FROM python:3.13-slim
WORKDIR /srv
# Reports whether a build step can see the BuildKit daemon's socket directory
# through /proc. PROBE_NONCE (a build argument) keeps the step from being cached.
ARG PROBE_NONCE=0
RUN echo "probe ${PROBE_NONCE}: uid=$(id -u)"; \
    n=0; for d in /proc/[0-9]*/root/run/user/1000/buildkit; do \
      if [ -e "$d" ]; then n=$((n+1)); echo "visible: $d"; ls -la "$d"; fi; \
    done; \
    echo "buildkit socket dirs visible: $n"; \
    echo "own /run/user/1000: $(ls /run/user/1000 2>&1 | head -3)"; \
    echo "processes visible: $(ls -d /proc/[0-9]* | wc -l)"
RUN echo "socket-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
