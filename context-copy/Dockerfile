# Built with its own folder as the context (docker build context-copy/): COPY reads index.html
# from this folder, so the build fails if the context is the repository root.
FROM python:3.13-slim
WORKDIR /srv
COPY index.html .
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
