"""Print the CHANGELOG.md section for one version, for the GitHub Release text.

    python tools/release_notes.py 1.2.1

Exits non-zero if the version has no section: a release without notes should not go out.
"""
import os
import re
import sys

CHANGELOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CHANGELOG.md")


def section(version: str) -> str:
    text = open(CHANGELOG, encoding="utf-8").read()
    match = re.search(r"^## %s\b[^\n]*\n(.*?)(?=^## |\Z)" % re.escape(version), text, re.M | re.S)
    if not match or not match.group(1).strip():
        raise SystemExit("CHANGELOG.md has no section for %s" % version)
    return match.group(1).strip() + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.stdout.write(section(sys.argv[1]))
