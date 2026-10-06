"""MkDocs hook: put the package version into the pages, taken from the code.

Write {{ version }} in a page and it becomes the version in discotoolkit/__init__.py, so the
documentation can never name a different version from the package it describes.
"""
import os
import re

_INIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "discotoolkit", "__init__.py")


def package_version() -> str:
    with open(_INIT, encoding="utf-8") as handle:
        return re.search(r'__version__\s*=\s*"([^"]+)"', handle.read()).group(1)


def on_page_markdown(markdown, **kwargs):
    return markdown.replace("{{ version }}", package_version())
