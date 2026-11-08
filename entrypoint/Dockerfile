FROM python:3.13-slim
WORKDIR /srv
RUN echo "entrypoint fixture" > index.html
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
