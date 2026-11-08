FROM python:3.13-slim
WORKDIR /srv
RUN echo "with-cmd fixture" > index.html
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
