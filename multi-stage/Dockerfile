FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90 AS build
RUN mkdir /out && echo "multi-stage fixture" > /out/index.html

FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
WORKDIR /srv
COPY --from=build /out/index.html .
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
