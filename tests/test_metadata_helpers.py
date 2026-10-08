"""
The metadata helpers people use to discover what they can filter on: list_all_columns and
list_metadata_item. No network: the metadata table is faked.

    python tests/test_metadata_helpers.py
"""
import os
import sys
from unittest import mock

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from discotoolkit import GetMetadata  # noqa: E402

TABLE = pd.DataFrame({
    "sample_id": ["S1", "S2", "S3"],
    "tissue": ["lung", "lung", "blood"],
    "platform": ["10x3'", "10x5'", "10x3'"],
})


def test_list_all_columns_names_every_metadata_field():
    with mock.patch.object(GetMetadata, "get_disco_metadata", return_value=TABLE):
        assert GetMetadata.list_all_columns() == ["sample_id", "tissue", "platform"]


def test_list_metadata_item_gives_each_value_once():
    with mock.patch.object(GetMetadata, "get_disco_metadata", return_value=TABLE):
        assert sorted(GetMetadata.list_metadata_item("platform")) == ["10x3'", "10x5'"]
        assert GetMetadata.list_metadata_item("no_such_field") is None


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
