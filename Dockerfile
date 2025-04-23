# Stage 1: Build (explicitly use x86_64)
FROM --platform=linux/amd64 python:3.11-slim-bookworm as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (match platform)
FROM --platform=linux/amd64 python:3.11-slim-bookworm

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y libpq5 && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY ./app /app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Make the start.sh script executable
RUN chmod +x /app/start.sh

EXPOSE 8000

# Use the start.sh script as the entry point
CMD ["/app/start.sh"]