#!/bin/bash

set -e

echo "==============================="
echo "  SHADOW BOT - PRE-FLIGHT CI  "
echo "==============================="

python scripts/preflight.py

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "==============================="
    echo "  ❌ BUILD FAILED"
    echo "  Bot will NOT start"
    echo "  Fix errors above"
    echo "==============================="
    echo ""

    # utrzymuje kontener ALIVE, ale bez restart loop
    # i z jasnym stanem
    while true; do
        sleep 3600
    done
fi

echo ""
echo "==============================="
echo "  ✅ PRE-FLIGHT OK"
echo "  STARTING BOT"
echo "==============================="
echo ""

exec python src/bootstrap/bot.py