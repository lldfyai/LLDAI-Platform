FROM python:3.11-slim

# Install Docker CLI with non-conflicting GID
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    groupmod -g 1001 docker && \
    useradd -u 1000 -g docker -m appuser && \
    mkdir -p /app && \
    chown appuser:docker /app

USER appuser

WORKDIR /app
COPY --chown=appuser:docker . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.main"]