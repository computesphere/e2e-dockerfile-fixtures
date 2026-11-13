FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# Reports the user namespace mappings a build step runs under, and fails the
# build if the step can write a host-wide kernel setting. The write puts back
# the value it read, so even a failing run changes nothing on the node.
# PROBE_NONCE (a build argument) keeps the step from being cached.
ARG PROBE_NONCE=0
RUN echo "probe ${PROBE_NONCE}: uid=$(id -u)"; \
    echo "uid_map self: $(tr -s ' ' < /proc/self/uid_map | tr '\n' ';')"; \
    echo "uid_map pid1: $(tr -s ' ' < /proc/1/uid_map 2>&1 | tr '\n' ';')"; \
    echo "gid_map pid1: $(tr -s ' ' < /proc/1/gid_map 2>&1 | tr '\n' ';')"; \
    cur=$(cat /proc/sys/kernel/core_pattern); \
    echo "core_pattern before: $cur"; \
    if [ -z "$cur" ]; then echo "core_pattern unreadable: FAIL"; exit 1; fi; \
    if (printf '%s\n' "$cur" > /proc/sys/kernel/core_pattern) 2>/dev/null; then \
      echo "host kernel setting writable (same value written back): FAIL"; \
      echo "core_pattern after: $(cat /proc/sys/kernel/core_pattern)"; exit 1; \
    else \
      echo "host kernel setting refused"; \
      echo "core_pattern after: $(cat /proc/sys/kernel/core_pattern)"; \
    fi
RUN echo "userns-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
