# Start with a modern, lightweight, official Python image.
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv pip install --no-cache-dir --system -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "app:app"]