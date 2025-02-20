FROM python:3.11-slim
# Disable VEX notice from Trivy
ENV TRIVY_DISABLE_VEX_NOTICE=true
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]
