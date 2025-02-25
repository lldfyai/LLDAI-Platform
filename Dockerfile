# Stage 1: Build (explicitly use x86_64)
FROM --platform=linux/amd64 python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (match platform)
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./app /app

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]