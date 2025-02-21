FROM python:3.11-slim

# Install Docker CLI and dependencies
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

# Create application user with docker group access
RUN groupadd -g 1001 dockergroup && \
    useradd -u 1001 -g dockergroup -m appuser && \
    usermod -aG docker appuser

USER appuser
WORKDIR /app

COPY --chown=appuser:dockergroup . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.main"]