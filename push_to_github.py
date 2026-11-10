
import subprocess
import sys
from pathlib import Path

PROJECT = Path(r"E:\SRAM-Stability-Analysis")
REPO = "https://github.com/adityaprasadmisra/SRAM.git"
BRANCH = "main"

EXCLUDED_DIRS = {
    ".git",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "node_modules"
}

EXCLUDED_FILES = {
    ".env"
}


def run(command, check=True):
    print("\n>", " ".join(map(str, command)))

    result = subprocess.run(
        command,
        cwd=PROJECT,
        text=True
    )

    if check and result.returncode != 0:
        print("\nERROR: Command failed.")
        sys.exit(result.returncode)

    return result.returncode


def main():
    if not PROJECT.exists():
        print("Project directory does not exist!")
        return

    # Initialize Git
    if not (PROJECT / ".git").exists():
        run(["git", "init"])

    run(["git", "branch", "-M", BRANCH])

    # Configure GitHub remote
    remotes = subprocess.run(
        ["git", "remote"],
        cwd=PROJECT,
        capture_output=True,
        text=True
    ).stdout.split()

    if "origin" in remotes:
        run(["git", "remote", "set-url", "origin", REPO])
    else:
        run(["git", "remote", "add", "origin", REPO])

    # Collect all project files
    files = []

    for path in PROJECT.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(PROJECT)

        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue

        if path.name in EXCLUDED_FILES:
            continue

        files.append(str(relative))

    print(f"\nTotal files found: {len(files)}")

    # Force-add every eligible file, including ignored images/data
    for i in range(0, len(files), 50):
        batch = files[i:i + 50]
        run(["git", "add", "-f", "--"] + batch)

    # Commit
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=PROJECT
    )

    if status.returncode == 1:
        run([
            "git", "commit",
            "-m", "Upload complete SRAM Stability Analysis project"
        ])
    elif status.returncode == 0:
        print("\nNo new changes to commit.")
    else:
        print("Could not inspect staged changes.")
        return

    # Check whether remote main already has commits
    remote = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", BRANCH],
        cwd=PROJECT,
        capture_output=True,
        text=True
    )

    if remote.returncode != 0:
        print(remote.stderr)
        return

    if remote.stdout.strip():
        print("\nRemote main already exists. Rebasing local commits...")
        run(["git", "pull", "--rebase", "origin", BRANCH])

    # Push everything
    run(["git", "push", "-u", "origin", BRANCH])

    print("\nPROJECT SUCCESSFULLY PUSHED!")
    print(REPO)


if __name__ == "__main__":
    main()
