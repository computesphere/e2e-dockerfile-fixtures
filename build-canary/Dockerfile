FROM busybox:1.37@sha256:a7dbc319b1438115a207e11930dc4bb3e643dcb3ec0bdd694bb36cd8fad289ec
WORKDIR /srv
# A small build that runs a step every time: CANARY_NONCE (a build argument)
# keeps the RUN from being cached, so the build really starts a container.
ARG CANARY_NONCE=0
COPY index.html .
RUN echo "build-canary ${CANARY_NONCE}: uid=$(id -u)" && test -s index.html
EXPOSE 8080
CMD ["sh", "-c", "httpd -f -p ${PORT:-8080} -h /srv"]
