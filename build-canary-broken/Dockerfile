FROM busybox:1.37@sha256:a7dbc319b1438115a207e11930dc4bb3e643dcb3ec0bdd694bb36cd8fad289ec
WORKDIR /srv
# The failing twin of build-canary/: its RUN step exits 1, so a build of it
# always fails. Used to prove that a failed build is reported.
ARG CANARY_NONCE=0
RUN echo "build-canary-broken ${CANARY_NONCE}: failing on purpose" && exit 1
CMD ["sh", "-c", "httpd -f -p ${PORT:-8080} -h /srv"]
