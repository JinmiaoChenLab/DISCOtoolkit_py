"""The version must be the same in setup.py and discotoolkit/__init__.py (and in the release tag).

Pure text checks, so they need no dependencies:

    python tests/test_version.py            # setup.py == __init__.py
    python tests/test_version.py v1.2.0     # ... and equals the tag
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def find(path, pattern):
    with open(os.path.join(ROOT, path)) as handle:
        match = re.search(pattern, handle.read())
    assert match, "no version found in %s" % path
    return match.group(1)


def test_setup_and_init_agree():
    setup_version = find("setup.py", r'version\s*=\s*"([^"]+)"')
    init_version = find("discotoolkit/__init__.py", r'__version__\s*=\s*"([^"]+)"')
    assert setup_version == init_version, "setup.py says %s, __init__.py says %s" % (setup_version, init_version)


def main():
    test_setup_and_init_agree()
    version = find("setup.py", r'version\s*=\s*"([^"]+)"')
    if len(sys.argv) > 1:
        tag = sys.argv[1]
        assert tag == "v" + version, "tag %s does not match package version %s (expected v%s)" % (tag, version, version)
    print("version %s OK" % version)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        sys.exit("FAIL: %s" % error)
