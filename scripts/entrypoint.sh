#!/bin/bash

echo "=== PRE-FLIGHT CHECK ==="

python scripts/preflight.py

if [ $? -ne 0 ]; then
    echo "=== BUILD FAILED - FIX ERRORS ABOVE ==="

    # zatrzymaj kontener bez restart loopa
    tail -f /dev/null
fi

echo "=== START BOT ==="

exec python src/bootstrap/bot.py