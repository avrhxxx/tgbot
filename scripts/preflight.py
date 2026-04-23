# scripts/preflight.py

import subprocess
import sys


def run(cmd: str):
    print(f"[PRECHECK] {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[FAILED] {cmd}")
        sys.exit(result.returncode)


def main():
    print("=== PRE-FLIGHT CHECK START ===")

    # 1. Lint + importy + basic errors
    run("ruff check src/")

    # 2. Type system check (ARCHITECTURE SAFETY)
    run("mypy src/")

    print("=== PRE-FLIGHT OK ===")


if __name__ == "__main__":
    main()