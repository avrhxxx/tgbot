#!/bin/bash

set -e

echo "====================================="
echo "     SHADOW BOT - BOOT SEQUENCE      "
echo "====================================="
echo ""

echo "[1/1] Running preflight CI gate..."
python -u scripts/preflight.py
EXIT_CODE=$?

echo ""

if [ $EXIT_CODE -ne 0 ]; then
    echo "====================================="
    echo "           ❌ BUILD FAILED            "
    echo "====================================="
    echo ""
    echo "Preflight failed. Runtime WILL NOT START."
    echo "Fix issues and redeploy."
    echo ""

    # 🔥 CRITICAL: EXIT, not sleep, not tail
    # to jest CI MODE, nie runtime mode
    exit 1
fi

echo "====================================="
echo "           ✅ BUILD OK                "
echo "         STARTING RUNTIME            "
echo "====================================="
echo ""

exec python -u src/bootstrap/bot.py