# scripts/preflight.py

import subprocess
import sys
from datetime import datetime


def run(cmd: str) -> int:
    print(f"\n[PRECHECK] $ {cmd}")
    print("-" * 60)

    result = subprocess.run(
        cmd,
        shell=True,
        text=True
    )

    if result.returncode != 0:
        print(f"\n[FAILED] {cmd}")

    return result.returncode


def main():
    print("\n===============================")
    print("  SHADOW BOT - PRE-FLIGHT CI")
    print(f"  {datetime.utcnow().isoformat()}Z")
    print("===============================\n")

    errors = 0

    # 1. Lint (ruff)
    print("\n>>> RUNNING RUFF")
    errors += run("ruff check src/")

    # 2. Type check (mypy)
    print("\n>>> RUNNING MYPY")
    errors += run("mypy src/")

    print("\n===============================")

    if errors > 0:
        print("❌ PRE-FLIGHT FAILED")
        print(f"❌ TOTAL ERROR SOURCES: {errors}")
        print("===============================\n")
        sys.exit(1)

    print("✅ PRE-FLIGHT PASSED")
    print("===============================\n")
    sys.exit(0)


if __name__ == "__main__":
    main()