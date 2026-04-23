FROM python:3.11-slim

WORKDIR /app

# =========================
# SYSTEM DEPENDENCIES
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# =========================
# PYTHON ENV
# =========================
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# =========================
# REQUIREMENTS
# =========================
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# =========================
# SOURCE CODE
# =========================
COPY . /app

# =========================
# STATIC ANALYSIS TOOLS
# =========================
RUN pip install ruff mypy

# =========================
# PORT (Railway/hosting)
# =========================
EXPOSE 8080

# =========================
# ENTRYPOINT
# =========================
CMD ["bash", "scripts/entrypoint.sh"]