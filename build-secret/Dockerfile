FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
# Needs a build secret with id FIXTURE_SECRET. Prints only its size, never the value.
RUN --mount=type=secret,id=FIXTURE_SECRET,required=true \
    echo "build secret present: $(wc -c < /run/secrets/FIXTURE_SECRET) bytes"
RUN echo "build-secret fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
