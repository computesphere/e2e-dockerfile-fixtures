FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# A build step (written as a heredoc) that tries what a container escape needs
# and reports each result, then makes one outbound HTTPS request:
# - unshare(CLONE_NEWUSER) and a tmpfs mount must be refused with EPERM; the
#   step exits 1 (failing the build) if either succeeds or fails another way;
# - chroot("/") is only reported (a default container profile allows it with
#   CAP_SYS_CHROOT);
# - an HTTPS GET to pypi.org is only reported (it needs outbound 443).
# Nothing here changes the host. The build argument PROBE_NONCE keeps the step
# from being cached.
ARG PROBE_NONCE=0
RUN python3 - <<'EOF'
import ctypes, errno, os, sys, urllib.request
nonce = os.environ.get("PROBE_NONCE", "0")
libc = ctypes.CDLL(None, use_errno=True)
def call(name, *args):
    r = getattr(libc, name)(*args)
    e = ctypes.get_errno()
    print(f"probe {nonce}: {name} returned {r} errno {e} ({errno.errorcode.get(e, '-')})", flush=True)
    return r, e
bad = []
r, e = call("unshare", 0x10000000)  # CLONE_NEWUSER
if not (r == -1 and e == errno.EPERM):
    bad.append("unshare(CLONE_NEWUSER)")
r, e = call("mount", b"none", b"/mnt", b"tmpfs", 0, None)
if not (r == -1 and e == errno.EPERM):
    bad.append("mount(tmpfs)")
call("chroot", b"/")
try:
    with urllib.request.urlopen("https://pypi.org/simple/pip/", timeout=20) as resp:
        print(f"probe {nonce}: https GET pypi.org status {resp.status}", flush=True)
except Exception as ex:
    print(f"probe {nonce}: https GET pypi.org failed: {type(ex).__name__}", flush=True)
if bad:
    print(f"probe {nonce}: NOT refused with EPERM: {', '.join(bad)}", flush=True)
    sys.exit(1)
print(f"probe {nonce}: escape calls refused", flush=True)
EOF
RUN echo "seccomp-step-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
