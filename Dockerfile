# Stage 1: Builder
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools==70.0.0 && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim-bookworm

WORKDIR /app

# Create non-root user
RUN addgroup --system appuser && \
    adduser --system --ingroup appuser appuser

# Install runtime dependencies (including git)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY --chown=appuser:appuser . .

# Security hardening
USER appuser

CMD ["python", "-m", "app.main"]