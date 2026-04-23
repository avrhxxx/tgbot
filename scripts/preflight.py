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

    run("ruff check src/")

    print("=== PRE-FLIGHT OK ===")


if __name__ == "__main__":
    main()