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
# STATIC TOOLS (preflight deps)
# =========================
RUN pip install ruff mypy

# =========================
# RAILWAY PORT
# =========================
EXPOSE 8080

# =========================
# ENTRYPOINT (JEDYNY FLOW)
# =========================
CMD ["sh", "scripts/entrypoint.sh"]