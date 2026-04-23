import subprocess
import sys


def run(cmd: str) -> int:
    print("\n" + "=" * 80)
    print(f"RUNNING: {cmd}")
    print("=" * 80, flush=True)

    result = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )

    # zawsze drukujemy pełny output w kontrolowany sposób
    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print(f"\n❌ FAILED: {cmd}\n", flush=True)

    return result.returncode


def main():
    print("\n===============================")
    print(" SHADOW BOT - PRE-FLIGHT CI")
    print("===============================\n", flush=True)

    errors = 0

    # =========================
    # RUFF (lint + imports)
    # =========================
    errors += run("ruff check src/")

    # =========================
    # MYPY (type system)
    # =========================
    errors += run("mypy src/")

    # =========================
    # FINAL REPORT
    # =========================
    print("\n===============================")

    if errors:
        print("❌ PRE-FLIGHT FAILED")
        print("===============================\n", flush=True)
        sys.exit(1)

    print("✅ PRE-FLIGHT OK")
    print("===============================\n", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()