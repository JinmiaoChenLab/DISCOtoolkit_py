"""
Every dependency in requirements.txt has an upper limit, so a new major release of pandas, numpy and the
rest cannot break a fresh install. A new dependency without one fails here. See RELEASING.md.

    python tests/test_requirements.py
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def requirements():
    with open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip() and not line.lstrip().startswith("#")]


def test_every_dependency_has_an_upper_limit():
    unlimited = [line for line in requirements() if not re.search(r"<=?\s*\d", line)]
    assert not unlimited, "no upper limit (add <next major): %s" % unlimited


def test_the_limits_leave_room_above_the_minimum():
    for line in requirements():
        low = re.search(r">=\s*([\d.]+)", line)
        high = re.search(r"<\s*([\d.]+)", line)
        if low and high:
            as_tuple = lambda text: tuple(int(part) for part in text.split("."))  # noqa: E731
            assert as_tuple(low.group(1)) < as_tuple(high.group(1)), line


def test_every_line_is_a_valid_requirement():
    from packaging.requirements import Requirement

    for line in requirements():
        Requirement(line)


def _run_all():
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("  PASS  %s" % name)
        except Exception as error:
            failed += 1
            print("  FAIL  %s\n          %s: %s" % (name, type(error).__name__, error))
    print("\n%d/%d passed" % (len(tests) - failed, len(tests)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_all())
