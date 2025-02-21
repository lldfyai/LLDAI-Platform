FROM python:3.11-slim

USER appuser
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.main"]