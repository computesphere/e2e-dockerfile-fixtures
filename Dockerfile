FROM busybox:1.36
# Starts, prints two lines and exits with an error, every time. Nothing listens on any port.
CMD ["sh", "-c", "echo starting; sleep 2; echo boom; exit 1"]
