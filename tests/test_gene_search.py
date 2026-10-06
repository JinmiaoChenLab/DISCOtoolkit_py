"""
gene_search draws with seaborn and matplotlib, which change between releases (a plot argument
that was ignored in one release is an error in the next). This runs the real plotting code on a
fake server answer, so a library upgrade that breaks it fails here instead of in a user's notebook.

    python tests/test_gene_search.py
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from unittest import mock  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from discotoolkit import GeneSearch  # noqa: E402

# [semicolon-separated values, cell type, (unused), atlas]
ROWS = [
    ["10;12;11;13;9;14", "T cell", "x", "thymus"],
    ["30;28;31;29;33;27", "Cardiomyocyte", "x", "heart"],
    ["3;4;2;5;3;4", "Fibroblast", "x", "heart"],
]


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return ROWS


def test_gene_search_draws_a_figure_for_all_atlases_and_for_a_subset():
    with mock.patch.object(GeneSearch.requests, "get", return_value=FakeResponse()):
        for atlas in (None, ["heart"], "thymus"):
            plt.close("all")
            drawn = []
            with mock.patch.object(plt, "show", lambda *a, **k: drawn.append(plt.gcf())):
                assert GeneSearch.gene_search("CD4", atlas=atlas, figsize=(6, 4), dpi=60) is None
            assert len(drawn) == 1 and drawn[0].axes, "no figure for atlas=%r" % (atlas,)


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
