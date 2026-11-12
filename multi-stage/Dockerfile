FROM python:3.13-slim AS build
RUN mkdir /out && echo "multi-stage fixture" > /out/index.html

FROM python:3.13-slim
WORKDIR /srv
COPY --from=build /out/index.html .
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
