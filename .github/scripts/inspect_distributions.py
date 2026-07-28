"""Inspect distribution archives for required and forbidden files.

Invoked by the TestPyPI publishing workflow after twine check
to verify distribution contents match expectations.
"""

import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

PACKAGE_MAP = {
    "featuresmith_core": {
        "wheel_source": "featuresmith/",
        "sdist_source": "src/featuresmith/",
        "name": "featuresmith-core",
    },
    "featuresmith_cli": {
        "wheel_source": "featuresmith_cli/",
        "sdist_source": "src/featuresmith_cli/",
        "name": "featuresmith-cli",
    },
}

FORBIDDEN_PREFIXES = [
    "tests/",
    "__pycache__/",
    ".gitignore",
    "node_modules/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".pytest_cache/",
    ".venv/",
    ".git/",
    ".idea/",
    ".vscode/",
    ".next/",
    "screenshots/",
]


def identify_package(filename: str) -> dict | None:
    for prefix, info in PACKAGE_MAP.items():
        if filename.startswith(prefix):
            return info
    return None


def check_wheel(path: Path, errors: list[str]) -> None:
    info = identify_package(path.name)
    if info is None:
        errors.append(f"[UNKNOWN] Cannot identify package for {path.name}")
        return

    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        print(f"\n  {'=' * 60}")
        print(f"  Wheel: {path.name} ({info['name']})")
        print(f"  {'=' * 60}")
        for name in names:
            print(f"    {name}")

        source_prefix = info["wheel_source"]

        # Required files for this package
        required = [
            f"{source_prefix}__init__.py",
            f"{source_prefix}py.typed",
            "LICENSE",
            ".dist-info/METADATA",
        ]

        for req in required:
            if not any(req in n for n in names):
                errors.append(f"[MISSING] {req} in {path.name}")

        # Forbidden files
        visited_tops = set()
        for name in names:
            path_obj = PurePosixPath(name)
            top = path_obj.parts[0] + "/" if path_obj.parts else ""
            if top in visited_tops:
                continue
            visited_tops.add(top)
            for forbid in FORBIDDEN_PREFIXES:
                if top == forbid or name == forbid or name.startswith(forbid):
                    errors.append(f"[FORBIDDEN] {name} in {path.name}")
                    break


def check_sdist(path: Path, errors: list[str]) -> None:
    info = identify_package(path.name)
    if info is None:
        errors.append(f"[UNKNOWN] Cannot identify package for {path.name}")
        return

    with tarfile.open(path, "r:gz") as t:
        names = t.getnames()
        print(f"\n  {'=' * 60}")
        print(f"  Source dist: {path.name} ({info['name']})")
        print(f"  {'=' * 60}")

        # Strip top-level directory from sdist entries
        stripped: list[str] = []
        for name in names:
            parts = PurePosixPath(name).parts
            s = PurePosixPath(*parts[1:]).as_posix() if len(parts) > 1 else name
            stripped.append(s)
            print(f"    {name}")

        source_prefix = info["sdist_source"]

        # Required files for this package
        required = [
            f"{source_prefix}__init__.py",
            f"{source_prefix}py.typed",
            "pyproject.toml",
            "LICENSE",
            "README.md",
        ]

        for req in required:
            if not any(req in s for s in stripped):
                errors.append(f"[MISSING] {req} in {path.name}")

        # Forbidden files
        visited_tops = set()
        for name in stripped:
            if not name:
                continue
            path_obj = PurePosixPath(name)
            top = path_obj.parts[0] + "/" if path_obj.parts else ""
            if top in visited_tops:
                continue
            visited_tops.add(top)
            for forbid in FORBIDDEN_PREFIXES:
                if top == forbid or name == forbid or name.startswith(forbid):
                    # Check it's not the legitimate source directory
                    if top == source_prefix:
                        continue
                    errors.append(f"[FORBIDDEN] {name} in {path.name}")
                    break


def main() -> None:
    dist_dir = Path("dist")
    if not dist_dir.is_dir():
        print("No dist/ directory found. Nothing to inspect.")
        return

    errors: list[str] = []

    print("=" * 64)
    print("  Distribution Content Inspection")
    print("=" * 64)

    for path in sorted(dist_dir.iterdir()):
        if path.suffix == ".whl":
            check_wheel(path, errors)
        elif path.suffix == ".gz" and path.name.endswith(".tar.gz"):
            check_sdist(path, errors)

    if errors:
        print(f"\n{'=' * 64}")
        print("  INSPECTION FAILED")
        print(f"  {len(errors)} issue(s) found:")
        for e in errors:
            print(f"    - {e}")
        print(f"{'=' * 64}")
        sys.exit(1)

    print(f"\n{'=' * 64}")
    print("  All distributions passed content inspection.")
    print(f"{'=' * 64}")


if __name__ == "__main__":
    main()
