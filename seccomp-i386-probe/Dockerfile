FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# Writes a 93-byte 32-bit x86 (i386) program whose only instructions are
# exit(0) through int 0x80, runs it once, and prints how it ended. Under a
# seccomp profile that lists only x86_64 a 32-bit system call meets the
# profile's bad-architecture action, so the expected line is "exit status 159"
# (128 + SIGSYS 31). A kernel without 32-bit support prints an exec error
# instead. The step itself always passes, so the build reports the status
# rather than failing. The build argument PROBE_NONCE keeps the step from
# being cached.
ARG PROBE_NONCE=0
RUN python3 - <<'EOF'
import struct
code = bytes([0xb8, 0x01, 0, 0, 0,   # mov eax, 1 (exit)
              0x31, 0xdb,            # xor ebx, ebx
              0xcd, 0x80])           # int 0x80
base, hdr = 0x08048000, 52 + 32
ehdr = (b"\x7fELF" + bytes([1, 1, 1]) + bytes(9)
        + struct.pack("<HHIIIIIHHHHHH", 2, 3, 1, base + hdr, 52, 0, 0, 52, 32, 1, 0, 0, 0))
phdr = struct.pack("<IIIIIIII", 1, 0, base, base, hdr + len(code), hdr + len(code), 5, 0x1000)
open("/srv/exit32", "wb").write(ehdr + phdr + code)
EOF
RUN chmod +x /srv/exit32; /srv/exit32; echo "probe ${PROBE_NONCE}: 32-bit exit32 exit status $?"
RUN echo "seccomp-i386-probe fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
