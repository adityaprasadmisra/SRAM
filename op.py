
import os
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(r"E:\SRAM-Stability-Analysis")
OUTPUT = ROOT / "project_inventory.txt"

# Exclude environments and Git internals from the main inventory
EXCLUDE_DIRS = {
    ".git",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".ipynb_checkpoints",
    ".pytest_cache",
    "node_modules"
}

if not ROOT.exists():
    raise FileNotFoundError(f"Project not found: {ROOT}")

lines = []
extension_counts = Counter()
folder_counts = defaultdict(int)
folder_sizes = defaultdict(int)

total_files = 0
total_size = 0
large_files = []

def format_size(size):
    if size >= 1024**3:
        return f"{size / 1024**3:.2f} GB"
    if size >= 1024**2:
        return f"{size / 1024**2:.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.2f} KB"
    return f"{size} B"

def scan(folder, depth=0):
    global total_files, total_size

    try:
        entries = sorted(
            folder.iterdir(),
            key=lambda p: (p.is_file(), p.name.lower())
        )
    except PermissionError:
        lines.append("  " * depth + "[ACCESS DENIED]")
        return

    for path in entries:
        if path.is_dir():
            if path.name in EXCLUDE_DIRS:
                continue

            lines.append("  " * depth + f"[DIR]  {path.name}/")
            scan(path, depth + 1)

        elif path.is_file():
            try:
                size = path.stat().st_size
            except OSError:
                continue

            total_files += 1
            total_size += size

            ext = path.suffix.lower() or "[no extension]"
            extension_counts[ext] += 1

            relative = path.relative_to(ROOT)
            parent = str(relative.parent)

            folder_counts[parent] += 1
            folder_sizes[parent] += size

            if size > 100 * 1024 * 1024:
                large_files.append((str(relative), size))

            lines.append(
                "  " * depth
                + f"[FILE] {path.name} ({format_size(size)})"
            )

lines.append("=" * 75)
lines.append("SRAM STABILITY ANALYSIS - PROJECT INVENTORY")
lines.append("=" * 75)
lines.append(f"Project root: {ROOT}")
lines.append("")

lines.append("COMPLETE DIRECTORY AND FILE TREE")
lines.append("-" * 75)

scan(ROOT)

lines.append("")
lines.append("=" * 75)
lines.append("PROJECT SUMMARY")
lines.append("=" * 75)
lines.append(f"Total files: {total_files}")
lines.append(f"Total size: {format_size(total_size)}")

lines.append("")
lines.append("FILE TYPES")
lines.append("-" * 75)

for ext, count in extension_counts.most_common():
    lines.append(f"{ext}: {count} files")

lines.append("")
lines.append("FOLDER SUMMARY")
lines.append("-" * 75)

for folder, count in sorted(folder_counts.items()):
    lines.append(
        f"{folder}: {count} files, "
        f"{format_size(folder_sizes[folder])}"
    )

lines.append("")
lines.append("FILES LARGER THAN 100 MB")
lines.append("-" * 75)

if large_files:
    for filename, size in large_files:
        lines.append(f"{filename}: {format_size(size)}")
else:
    lines.append("None found.")

OUTPUT.write_text("\n".join(lines), encoding="utf-8")

print("\nInventory completed!")
print(f"Total files: {total_files}")
print(f"Total size: {format_size(total_size)}")
print(f"File types found: {len(extension_counts)}")
print(f"Files above 100 MB: {len(large_files)}")
print(f"\nInventory saved at:\n{OUTPUT}")
