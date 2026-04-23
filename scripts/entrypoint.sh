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
    echo ""

    # HARD STOP STATE (NO RESTART LOOP)
    # Railway zobaczy proces jako "alive", ale bez crash loop
    tail -f /dev/null
fi

echo "====================================="
echo "           ✅ BUILD OK                "
echo "         STARTING RUNTIME            "
echo "====================================="
echo ""

exec python src/bootstrap/bot.py