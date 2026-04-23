FROM python:3.11-slim

WORKDIR /app

# =========================
# SYSTEM DEPENDENCIES
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# =========================
# PYTHON PATH FIX
# =========================
ENV PYTHONPATH=/app

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
# PRE-FLIGHT CHECKS
# =========================
# (TS-like safety gate before runtime)
RUN pip install ruff

# =========================
# RAILWAY PORT
# =========================
EXPOSE 8080

# =========================
# START (SAFE ENTRYPOINT)
# =========================
CMD ["sh", "-c", "python scripts/preflight.py && python src/bootstrap/bot.py"]