# ===============================
# Shadow Bot - Dockerfile
# Path: /Dockerfile
# Layer: Runtime / Deployment
# ===============================

FROM python:3.11-slim

# Prevent .pyc files + ensure logs are flushed
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System dependencies (minimal, safe for aiogram + google + async)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (cache optimization)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Default command (always entrypoint controlled)
CMD ["/bin/bash", "/app/entrypoint.sh"]