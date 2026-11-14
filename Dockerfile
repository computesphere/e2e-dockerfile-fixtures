FROM busybox:1.36@sha256:73aaf090f3d85aa34ee199857f03fa3a95c8ede2ffd4cc2cdb5b94e566b11662
# Starts, prints two lines and exits with an error, every time. Nothing listens on any port.
CMD ["sh", "-c", "echo starting; sleep 2; echo boom; exit 1"]
