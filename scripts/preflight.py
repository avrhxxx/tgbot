# scripts/preflight.py

import subprocess
import sys


def run(cmd: str):
    print(f"\n>>> RUNNING: {cmd}\n", flush=True)

    result = subprocess.run(
        cmd,
        shell=True,
        text=True
    )

    return result.returncode


def main():
    print("\n===============================")
    print("  SHADOW BOT - PRE-FLIGHT CI   ")
    print("===============================\n", flush=True)

    errors = 0

    # 1. Ruff (full report, no suppression)
    errors += run("ruff check src/")

    # 2. Mypy (single run, no partial interruption noise)
    errors += run("mypy src/")

    print("\n===============================")

    if errors != 0:
        print("❌ PRE-FLIGHT FAILED")
        print("Fix errors above and redeploy.")
        print("===============================\n")
        sys.exit(1)

    print("✅ PRE-FLIGHT OK")
    print("===============================\n")

    sys.exit(0)


if __name__ == "__main__":
    main()