FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# Makes exactly one uselib(NULL) system call (x86_64 number 134) in one build
# step, from python3. Default container seccomp profiles don't allow uselib,
# so a profile that logs what it doesn't allow records this call once: a known
# positive for counting a build's seccomp records. The call itself does
# nothing (NULL path); the build passes whatever it returns. The build
# argument PROBE_NONCE keeps the step from being cached.
ARG PROBE_NONCE=0
RUN python3 -c "import ctypes, os; libc = ctypes.CDLL(None, use_errno=True); r = libc.syscall(134, None); print('probe ${PROBE_NONCE}: pid', os.getpid(), 'uselib(NULL) returned', r, 'errno', ctypes.get_errno())"
RUN echo "seccomp-log-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
