
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(r"E:\SRAM-Stability-Analysis")
REPO_URL = "https://github.com/adityaprasadmisra/SRAM.git"
BRANCH = "main"


def run(command):
    print(f"\n>>> {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=PROJECT_DIR,
        text=True
    )

    if result.returncode != 0:
        print("\nCommand failed. Check the error above.")
        sys.exit(result.returncode)


def main():
    if not PROJECT_DIR.exists():
        print("Project directory not found!")
        return

    # Initialize Git if necessary
    if not (PROJECT_DIR / ".git").exists():
        run(["git", "init"])

    # Set branch
    run(["git", "branch", "-M", BRANCH])

    # Configure remote
    remotes = subprocess.run(
        ["git", "remote"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    ).stdout.split()

    if "origin" in remotes:
        run(["git", "remote", "set-url", "origin", REPO_URL])
    else:
        run(["git", "remote", "add", "origin", REPO_URL])

    # Stage entire project
    run(["git", "add", "-A"])

    # Commit
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=PROJECT_DIR
    )

    if status.returncode == 1:
        run([
            "git", "commit", "-m",
            "Initial commit: SRAM Stability Analysis"
        ])
    elif status.returncode == 0:
        print("\nNo new changes to commit.")
    else:
        print("Could not check staged changes.")
        return

    # Push
    run(["git", "push", "-u", "origin", BRANCH])

    print("\nSUCCESS! Project pushed to GitHub.")
    print(REPO_URL)


if __name__ == "__main__":
    main()
