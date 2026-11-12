FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# Fails the build if a build step can see a BuildKit daemon socket directory
# through /proc. PROBE_NONCE (a build argument) keeps the step from being cached.
ARG PROBE_NONCE=0
RUN n=0; for d in /proc/[0-9]*/root/run/user/1000/buildkit; do \
      if [ -e "$d" ]; then n=$((n+1)); fi; \
    done; \
    echo "buildkit socket dirs visible: $n"; \
    echo "probe ${PROBE_NONCE}: uid=$(id -u), processes visible: $(ls -d /proc/[0-9]* | wc -l)"; \
    for d in /proc/[0-9]*/root/run/user/1000/buildkit; do \
      if [ -e "$d" ]; then echo "visible: $d"; ls -la "$d"; fi; \
    done; \
    [ "$n" -eq 0 ]
RUN echo "socket-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
