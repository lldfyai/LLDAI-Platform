FROM python:3.11-slim

# Install Docker CLI and dependencies
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

# Create a docker group and add non-root user
RUN groupadd -g 999 docker && \
    useradd -u 1000 -g docker -m appuser && \
    mkdir -p /var/run/docker.sock

USER appuser

WORKDIR /app
COPY --chown=appuser:docker . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.main"]