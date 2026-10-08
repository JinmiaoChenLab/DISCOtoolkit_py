"""
Run every tutorial notebook in docs/ against a live DISCO server and save the outputs in place.

Why: the notebooks are the documentation, and a notebook whose saved output came from an old
run is documentation that lies. Executing them on every docs build means the pages show what
the current code and the current server really do, and a notebook that no longer works fails
the build instead of failing a user.

    python tools/execute_notebooks.py                    # all notebooks in docs/
    python tools/execute_notebooks.py docs/Gene_search.ipynb
    DISCO_API_URL=http://127.0.0.1:8889/disco_v3_api/ python tools/execute_notebooks.py

Cells tagged `skip-execution` are not run (the Colab-only `!pip install` cell, which would
replace the code being tested with the PyPI release). Each notebook runs in its own empty
temporary directory, so downloads never land in the repository.
"""
import argparse
import glob
import os
import re
import sys
import tempfile
import time

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

# Output that is true but not worth a reader's attention, and would only show this machine's paths.
ANSI = re.compile(r"\x1b\[[0-9;]*m")   # colour codes in tracebacks make CI logs unreadable
NOISE = re.compile(r"^\.\.\. storing '.*' as categorical\s*$")

# The notebooks run in a kernel that inherits this environment: no warnings (they quote file paths
# on the build machine), no progress bars, and figures drawn inline whatever the shell exported.
KERNEL_ENV = {
    "PYTHONWARNINGS": "ignore",
    "TQDM_DISABLE": "1",
    "MPLBACKEND": "module://matplotlib_inline.backend_inline",
}

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "docs")


def tidy(nb) -> None:
    """Show log lines as plain output rather than red error blocks, and drop the noise."""
    for cell in nb.cells:
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream":
                output["name"] = "stdout"
                output["text"] = "".join(
                    line for line in output["text"].splitlines(True) if not NOISE.match(line)
                )
        cell["outputs"] = [
            o for o in cell.get("outputs", []) if o.get("output_type") != "stream" or o["text"].strip()
        ]


def clear(path: str) -> None:
    """Remove outputs: committed notebooks carry none, so there is never a stale result to trust."""
    with open(path, encoding="utf-8") as handle:
        nb = nbformat.read(handle, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        cell.get("metadata", {}).pop("execution", None)
    nbformat.validator.normalize(nb)
    with open(path, "w", encoding="utf-8") as handle:
        nbformat.write(nb, handle)


def execute(path: str, timeout: int, include_skipped: bool = False) -> None:
    with open(path, encoding="utf-8") as handle:
        nb = nbformat.read(handle, as_version=4)
    with tempfile.TemporaryDirectory(prefix="disco-nb-") as workdir:
        client = NotebookClient(
            nb,
            timeout=timeout,
            kernel_name="python3",
            resources={"metadata": {"path": workdir}},
            # --as-user runs every cell, the Colab install cell included, as a reader would
            skip_cells_with_tag="no-such-tag" if include_skipped else "skip-execution",
            allow_errors=False,
        )
        client.execute()
    tidy(nb)
    # keep the file small and the diff readable: no per-run noise in the metadata
    for cell in nb.cells:
        cell.get("metadata", {}).pop("execution", None)
    nb.metadata.pop("widgets", None)
    with open(path, "w", encoding="utf-8") as handle:
        nbformat.write(nb, handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("notebooks", nargs="*", help="default: every .ipynb in docs/")
    parser.add_argument("--clear", action="store_true", help="remove the outputs instead of running")
    parser.add_argument("--as-user", action="store_true",
                        help="run every cell, including the Colab-only install cell (tests the PyPI release)")
    parser.add_argument("--timeout", type=int, default=900, help="seconds allowed per cell")
    args = parser.parse_args()

    paths = args.notebooks or sorted(glob.glob(os.path.join(DOCS, "*.ipynb")))
    if args.clear:
        for path in paths:
            clear(path)
        print("cleared %d notebooks" % len(paths))
        return 0
    os.environ.update(KERNEL_ENV)
    failed = []
    for path in paths:
        started = time.time()
        try:
            execute(path, args.timeout, args.as_user)
            print("  OK    %-40s %4.0fs" % (os.path.basename(path), time.time() - started), flush=True)
        except CellExecutionError as error:
            failed.append(path)
            print("  FAIL  %s\n%s" % (os.path.basename(path), ANSI.sub("", str(error))[-2500:]), flush=True)
    print("\n%d/%d notebooks ran" % (len(paths) - len(failed), len(paths)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
