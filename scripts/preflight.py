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

    failed = False

    # RUFF
    failed |= run("ruff check src/") != 0

    # MYPY
    failed |= run("mypy src/") != 0

    print("\n===============================")

    if failed:
        print("❌ PRE-FLIGHT FAILED")
        print("===============================\n", flush=True)
        sys.exit(1)

    print("✅ PRE-FLIGHT OK")
    print("===============================\n", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()