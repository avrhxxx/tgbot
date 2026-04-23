#!/bin/bash

set -e  # 🔴 KLUCZ: zatrzymaj build przy pierwszym błędzie

echo "=== PRE-FLIGHT CHECK ==="

python scripts/preflight.py

echo "=== START BOT ==="

exec python src/bootstrap/bot.py