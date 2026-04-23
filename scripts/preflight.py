# scripts/preflight.py

import subprocess
import sys


def run(cmd: str) -> int:
    print(f"[PRECHECK] {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[FAILED] {cmd}")
    return result.returncode


def main():
    print("=== PRE-FLIGHT CHECK START ===")

    errors = 0

    # 1. Lint + importy + basic errors (FULL REPORT)
    errors += run("ruff check src/")

    # 2. Type system check (TS-like safety)
    errors += run("mypy src/")

    if errors != 0:
        print("=== BUILD FAILED - FIX ERRORS ABOVE ===")
        sys.exit(1)

    print("=== PRE-FLIGHT OK ===")


if __name__ == "__main__":
    main()