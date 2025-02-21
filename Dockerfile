FROM python:3.11-slim
ENV TRIVY_DISABLE_VEX_NOTICE=true
WORKDIR /app

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.main"]