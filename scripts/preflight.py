import subprocess
import sys


def run(cmd: str):
    print("\n" + "=" * 60)
    print(f"RUNNING: {cmd}")
    print("=" * 60 + "\n", flush=True)

    result = subprocess.run(
        cmd,
        shell=True,
        text=True
    )

    return result.returncode


def main():
    print("\n===============================")
    print(" SHADOW BOT - PRE-FLIGHT CI")
    print("===============================\n", flush=True)

    errors = 0

    # Ruff
    errors += run("ruff check src/")

    # Mypy
    errors += run("mypy src/")

    print("\n===============================")

    if errors:
        print("❌ PRE-FLIGHT FAILED")
        print("===============================\n")
        sys.exit(1)

    print("✅ PRE-FLIGHT OK")
    print("===============================\n")
    sys.exit(0)


if __name__ == "__main__":
    main()