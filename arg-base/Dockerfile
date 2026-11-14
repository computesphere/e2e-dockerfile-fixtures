# The base image is a build argument, BASE. Unset, it is with-cmd's base.
ARG BASE=python:3.13-slim
FROM ${BASE}
WORKDIR /srv
RUN echo "arg-base fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
