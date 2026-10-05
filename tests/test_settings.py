"""Offline tests for choosing a DISCO server. No network, and no pandas/scanpy needed:
GlobalVariable is loaded straight from its file, so this runs on any Python >= 3.9.

    python tests/test_settings.py        or        pytest tests/test_settings.py
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "discotoolkit", "GlobalVariable.py")


def load(env=None):
    """A fresh copy of GlobalVariable, as if the package had just been imported."""
    saved = os.environ.get("DISCO_API_URL")
    if env is None:
        os.environ.pop("DISCO_API_URL", None)
    else:
        os.environ["DISCO_API_URL"] = env
    try:
        spec = importlib.util.spec_from_file_location("GlobalVariable_under_test", PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if saved is None:
            os.environ.pop("DISCO_API_URL", None)
        else:
            os.environ["DISCO_API_URL"] = saved


def test_default_server_is_disco_v1():
    g = load()
    assert g.get_server() == "https://disco.bii.a-star.edu.sg/disco_v3_api/"


def test_api_url_joins_paths_with_exactly_one_slash():
    g = load()
    assert g.api_url("toolkit/getSampleMetadata") == g.get_server() + "toolkit/getSampleMetadata"
    assert g.api_url("/toolkit/getSampleMetadata") == g.get_server() + "toolkit/getSampleMetadata"


def test_named_presets_and_urls():
    g = load()
    assert g.set_server("v2") == "https://immunesinglecell.org/disco_v3_api/"
    assert g.api_url("x") == "https://immunesinglecell.org/disco_v3_api/x"      # takes effect at once
    assert g.set_server("V1") == g.SERVERS["v1"]                                 # preset names are case-insensitive
    assert g.set_server("https://example.org/api") == "https://example.org/api/"  # trailing slash added
    assert g.set_server("http://localhost:8889/disco_v3_api///") == "http://localhost:8889/disco_v3_api/"


def test_bad_servers_are_rejected_without_changing_the_current_one():
    g = load()
    before = g.get_server()
    for bad in ["", "   ", "v3", "ftp://x", "disco.bii.a-star.edu.sg", None, 5]:
        try:
            g.set_server(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("accepted %r" % (bad,))
    assert g.get_server() == before


def test_environment_variable_sets_the_starting_server():
    assert load("v2").get_server() == "https://immunesinglecell.org/disco_v3_api/"
    assert load("https://example.org/disco_v3_api").get_server() == "https://example.org/disco_v3_api/"


def test_old_prefix_variable_still_readable():
    g = load()
    g.set_server("v2")
    assert g.prefix_disco_url == "https://immunesinglecell.org/disco_v3_api/"


def _run_all():
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn(); print("  PASS  %s" % name)
        except Exception as error:
            failed += 1; print("  FAIL  %s\n          %s: %s" % (name, type(error).__name__, error))
    print("\n%d/%d passed" % (len(tests) - failed, len(tests)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_all())
