FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
COPY server.py .
EXPOSE 3000
# Runs as nobody (65534): the app needs no write access and no root.
USER 65534:65534
CMD ["python", "-u", "server.py"]
