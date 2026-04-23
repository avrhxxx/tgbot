#!/bin/bash

set -e

echo "====================================="
echo "     SHADOW BOT - BOOT SEQUENCE      "
echo "====================================="

echo ""
echo "[1/2] Running preflight checks..."

python scripts/preflight.py
EXIT_CODE=$?

echo ""

if [ $EXIT_CODE -ne 0 ]; then
    echo "====================================="
    echo "           ❌ BUILD FAILED            "
    echo "     BOT WILL NOT START RUNTIME      "
    echo "====================================="
    echo ""
    echo "Fix errors and redeploy manually."
    echo "Container will stay ALIVE (no crash loop)."
    echo ""

    # 🔒 HARD LOCK STATE (NO EXIT, NO RESTART LOOP)
    # Railway keeps container alive, but stable
    while true; do
        sleep 3600
    done
fi

echo "====================================="
echo "           ✅ BUILD OK                "
echo "         STARTING RUNTIME            "
echo "====================================="
echo ""

exec python src/bootstrap/bot.py