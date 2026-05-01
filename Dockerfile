# ===============================
# Shadow Bot - Dockerfile
# ===============================

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# system deps (minimal)
RUN apt-get update && apt-get install -y \
    gcc curl \
    && rm -rf /var/lib/apt/lists/*

# dependencies first (cache layer)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . /app

# entrypoint permissions
RUN chmod +x /app/entrypoint.sh

CMD ["bash", "/app/entrypoint.sh"]