#!/bin/bash

set -e

echo "=== PRE-FLIGHT CHECK ==="

python scripts/preflight.py

echo "=== START BOT ==="

exec python src/bootstrap/bot.py