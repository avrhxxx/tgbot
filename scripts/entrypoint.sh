#!/bin/bash

set -e

LOCK="/tmp/shadow_preflight_done.lock"

echo "====================================="
echo "     SHADOW BOT - BOOT SEQUENCE      "
echo "====================================="

if [ -f "$LOCK" ]; then
    echo "[ENTRYPOINT] Preflight already executed - EXITING DUPLICATE PROCESS"
    exit 0
fi

touch "$LOCK"

echo "[ENTRYPOINT] Running preflight ONCE..."

python -u scripts/preflight.py
EXIT_CODE=$?

echo ""

if [ $EXIT_CODE -ne 0 ]; then
    echo "====================================="
    echo "           ❌ BUILD FAILED            "
    echo "====================================="
    echo "Stopping process (no restart, no loop)"
    echo "====================================="

    exit 1
fi

echo "====================================="
echo "           ✅ BUILD OK                "
echo "         STARTING RUNTIME            "
echo "====================================="

exec python -u src/bootstrap/bot.py