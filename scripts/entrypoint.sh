#!/bin/bash

echo "==============================="
echo "  SHADOW BOT - PRE-FLIGHT CI  "
echo "==============================="

set +e
python scripts/preflight.py
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "==============================="
    echo "  ❌ BUILD FAILED"
    echo "  Bot will NOT start"
    echo "==============================="
    echo ""

    # HARD STOP MODE (bez restart loop triggerowania Railway)
    tail -f /dev/null
fi

echo ""
echo "==============================="
echo "  ✅ PRE-FLIGHT OK"
echo "  STARTING BOT"
echo "==============================="
echo ""

exec python src/bootstrap/bot.py