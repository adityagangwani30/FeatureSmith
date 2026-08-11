"""Execution and validation script for Featuresmith Jupyter notebooks."""

import io
import json
import os
import sys
from pathlib import Path


def execute_notebook(nb_path: Path) -> bool:
    print(f"Executing notebook: {nb_path.name} ...")
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)

    # Global environment for execution
    exec_env = {"__name__": "__main__"}

    # Change CWD to notebook directory during execution so relative paths work
    orig_cwd = os.getcwd()
    os.chdir(nb_path.parent)

    cell_count = 0
    try:
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                cell_count += 1
                code_text = "".join(cell["source"])

                # Capture stdout
                stdout_capture = io.StringIO()
                orig_stdout = sys.stdout
                sys.stdout = stdout_capture

                try:
                    exec(code_text, exec_env)
                except Exception as e:
                    sys.stdout = orig_stdout
                    print(f"[FAILED] Error in {nb_path.name} (Cell {cell_count}): {e}")
                    os.chdir(orig_cwd)
                    return False
                finally:
                    sys.stdout = orig_stdout

                output_text = stdout_capture.getvalue()
                cell["execution_count"] = cell_count
                cell["outputs"] = [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": output_text.splitlines(keepends=True),
                    }
                ]

        # Save populated notebook back
        os.chdir(orig_cwd)
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=2)

        print(
            f"[PASSED] {nb_path.name} executed successfully ({cell_count} code cells executed)."
        )
        return True

    except Exception as exc:
        os.chdir(orig_cwd)
        print(f"[FAILED] Exception executing {nb_path.name}: {exc}")
        return False


def main():
    nb_dir = Path("examples/notebooks")
    notebooks = sorted(nb_dir.glob("*.ipynb"))

    if not notebooks:
        print("No notebooks found in examples/notebooks.")
        sys.exit(1)

    all_passed = True
    for nb in notebooks:
        passed = execute_notebook(nb)
        if not passed:
            all_passed = False

    if not all_passed:
        print("\n[FAILED] Notebook execution failed.")
        sys.exit(1)

    print(
        f"\n[SUCCESS] All {len(notebooks)} Jupyter Notebooks executed and validated successfully!"
    )


if __name__ == "__main__":
    main()
