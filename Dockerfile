FROM python:3.11-slim

WORKDIR /app

# =========================
# SYSTEM DEPENDENCIES
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# =========================
# REQUIREMENTS
# =========================
COPY requirements/ /app/requirements/

RUN pip install --no-cache-dir -r requirements/production.txt

# =========================
# CODE
# =========================
COPY . /app

# =========================
# RAILWAY PORT
# =========================
EXPOSE 8080

# =========================
# START
# =========================
CMD ["python", "bot.py"]