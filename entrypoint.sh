#!/bin/bash

set -e

LOCK="/tmp/shadow_bot.lock"

if [ -f "$LOCK" ]; then
    echo "[ENTRYPOINT] Already executed - exit"
    exit 0
fi

touch "$LOCK"

echo "[CI] Running preflight..."

python -u scripts/preflight.py
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "==============================="
    echo " ❌ PRE-FLIGHT FAILED"
    echo "==============================="
    echo ""
    exit 1
fi

echo "[CI] OK - starting runtime"

# 🔥 FIX: allow `src.*` imports
export PYTHONPATH=/app

exec python -u src/bootstrap/bot.py