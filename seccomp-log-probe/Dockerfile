FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# Two system calls from python3 in one build step, each made exactly once:
# - socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE), closed straight away. BuildKit's
#   own default profile for build steps allows it; an outer profile that allows
#   only some socket families and logs the rest records it once. This is the known positive.
# - uselib(NULL) (x86_64 number 134). BuildKit's own profile for build steps
#   refuses it (EPERM), so no outer profile ever sees it: the known negative.
# Both calls do nothing lasting; the build passes whatever they return. The
# build argument PROBE_NONCE keeps the step from being cached.
ARG PROBE_NONCE=0
RUN python3 -c "import ctypes, os, socket; libc = ctypes.CDLL(None, use_errno=True); s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, 0); s.close(); r = libc.syscall(134, None); print('probe ${PROBE_NONCE}: pid', os.getpid(), 'netlink route socket opened and closed; uselib(NULL) returned', r, 'errno', ctypes.get_errno())"
RUN echo "seccomp-log-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
