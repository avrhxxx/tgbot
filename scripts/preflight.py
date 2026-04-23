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

    # Static linting (fast fail)
    run("ruff check src/")

    # Type checking (optional but now enabled TS-like gate)
    run("mypy src/")

    print("=== PRE-FLIGHT OK ===")


if __name__ == "__main__":
    main()