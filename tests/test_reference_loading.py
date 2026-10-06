"""
_load_reference: the CELLiD reference tables are downloaded once, as CSV when the server has it,
and fall back to the old pickle when it does not. No network: the server is faked.

    python tests/test_reference_loading.py
"""
import os
import sys
import tempfile
from unittest import mock

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from discotoolkit import CELLiD  # noqa: E402

CSV = b'"","T cell--atlas_a","B cell--atlas_a"\n"CD4",1.5,0.0\n"MS4A1",0.0,2.5\n'


class FakeResponse:
    def __init__(self, status, body=b""):
        self.status_code = status
        self.content = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def iter_content(self, chunk_size=None):
        yield self.content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError("HTTP %s" % self.status_code)


def server(csv_status, calls):
    def get(url, params=None, **kwargs):
        calls.append((url.rsplit("/", 1)[-1], (params or {}).get("type")))
        if (params or {}).get("type") == "csv":
            return FakeResponse(csv_status, CSV if csv_status == 200 else b"")
        # the pickle fallback: a gzip pickle of a small table
        path = os.path.join(tempfile.gettempdir(), "disco_fake.pkl")
        pd.DataFrame({"gene": ["CD4"], "group": ["T cell--a"]}).to_pickle(
            path, compression={"method": "gzip", "compresslevel": 6}
        )
        return FakeResponse(200, open(path, "rb").read())

    return get


def test_csv_is_downloaded_once_and_read_with_genes_as_index():
    calls = []
    with tempfile.TemporaryDirectory() as d, mock.patch.object(CELLiD.requests, "get", server(200, calls)):
        first = CELLiD._load_reference(d, "ref_data", "getRef", index_col=0)
        again = CELLiD._load_reference(d, "ref_data", "getRef", index_col=0)
        assert list(first.index) == ["CD4", "MS4A1"] and list(first.columns)[0] == "T cell--atlas_a"
        assert first.equals(again)
        assert calls == [("getRef", "csv")], "second call must use the saved file: %s" % calls
        assert not os.path.exists(os.path.join(d, "ref_data.csv.part"))


def test_old_server_without_csv_falls_back_to_the_pickle():
    calls = []
    with tempfile.TemporaryDirectory() as d, mock.patch.object(CELLiD.requests, "get", server(400, calls)):
        deg = CELLiD._load_reference(d, "ref_deg", "getRefDeg")
        assert list(deg.columns) == ["gene", "group"]
        assert calls == [("getRefDeg", "csv"), ("getRefDeg", "pkl")], calls


def test_a_pickle_saved_by_an_earlier_version_is_still_used():
    calls = []
    with tempfile.TemporaryDirectory() as d, mock.patch.object(CELLiD.requests, "get", server(200, calls)):
        pd.DataFrame({"gene": ["X"], "group": ["g"]}).to_pickle(
            os.path.join(d, "ref_deg.pkl"), compression={"method": "gzip", "compresslevel": 6}
        )
        deg = CELLiD._load_reference(d, "ref_deg", "getRefDeg")
        assert list(deg["gene"]) == ["X"] and calls == [], "must not touch the network"


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
