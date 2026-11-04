
import os
import subprocess
import sys

# Project configuration
PROJECT_PATH = r"E:\SRAM-Stability-Analysis"
GITHUB_REPO = (
    "https://github.com/adityaprasadmisra/"
    "SRAM-Error-Analysis.git"
)
BRANCH = "main"
COMMIT_MESSAGE = "Initial commit: SRAM Error Analysis and ML pipeline"


def run_command(command):
    print(f"\n>>> {' '.join(command)}")

    result = subprocess.run(
        command,
        cwd=PROJECT_PATH,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}"
        )

    return result


def main():
    try:
        if not os.path.isdir(PROJECT_PATH):
            raise FileNotFoundError(
                f"Project folder not found: {PROJECT_PATH}"
            )

        os.chdir(PROJECT_PATH)

        print("=" * 55)
        print("       SRAM PROJECT - GITHUB UPLOADER")
        print("=" * 55)

        # Check Git installation
        run_command(["git", "--version"])

        # Initialize repository
        if not os.path.isdir(".git"):
            run_command(["git", "init"])

        # Set branch
        run_command(["git", "branch", "-M", BRANCH])

        # Configure remote
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True
        )

        if remote.returncode == 0:
            run_command([
                "git", "remote", "set-url",
                "origin", GITHUB_REPO
            ])
        else:
            run_command([
                "git", "remote", "add",
                "origin", GITHUB_REPO
            ])

        # Stage all files
        run_command(["git", "add", "-A"])

        # Display staged files
        print("\nFiles prepared for upload:")
        run_command(["git", "status", "--short"])

        # Confirm before committing and pushing
        confirm = input(
            "\nProceed with commit and GitHub push? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("Upload cancelled.")
            return

        # Check whether there are staged changes
        staged = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=PROJECT_PATH
        )

        if staged.returncode == 1:
            run_command([
                "git", "commit", "-m", COMMIT_MESSAGE
            ])
        elif staged.returncode == 0:
            print("\nNo new changes to commit.")
        else:
            raise RuntimeError("Could not inspect staged changes.")

        # Push to GitHub
        run_command([
            "git", "push", "-u", "origin", BRANCH
        ])

        print("\n" + "=" * 55)
        print("       PROJECT PUSHED SUCCESSFULLY!")
        print("=" * 55)
        print(f"Repository: {GITHUB_REPO}")

    except Exception as error:
        print(f"\nERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
