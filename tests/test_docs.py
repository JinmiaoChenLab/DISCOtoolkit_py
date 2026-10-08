"""
The documentation is built from this repository on every change. These checks keep it honest and
need no network and no third-party packages:

  * the committed notebooks carry no saved output (the build re-runs them against the live
    database, so a saved output could only ever be stale);
  * every page in the navigation exists;
  * every public function of the package appears in the API reference, so a new function cannot
    ship undocumented.

    python tests/test_docs.py
"""
import ast
import glob
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# helpers that are not part of the public interface
INTERNAL = {
    "api_url", "check_in_list", "generate_correlation_map", "get_disco_metadata", "get_json",
    "get_sample_ct_info", "write_10X_h5",
}


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return handle.read()


def test_committed_notebooks_have_no_saved_output():
    dirty = []
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "*.ipynb"))):
        for cell in json.load(open(path, encoding="utf-8"))["cells"]:
            if cell["cell_type"] == "code" and (cell.get("outputs") or cell.get("execution_count")):
                dirty.append(os.path.basename(path))
                break
    assert not dirty, "run `python tools/execute_notebooks.py --clear` on: %s" % ", ".join(dirty)


def test_every_page_in_the_navigation_exists():
    nav = read("mkdocs.yml").split("nav:")[1].split("\nplugins:")[0]
    pages = re.findall(r":\s+([\w./-]+\.(?:md|ipynb))\s*$", nav, re.M)
    assert pages, "found no pages in mkdocs.yml"
    missing = [p for p in pages if not os.path.exists(os.path.join(ROOT, "docs", p))]
    assert not missing, "in mkdocs.yml but not in docs/: %s" % missing


def test_every_public_function_is_in_the_api_reference():
    api = read("docs/API.md")
    documented = set(re.findall(r"^:::\s+discotoolkit\.\w+\.(\w+)", api, re.M))
    public = set()
    for path in glob.glob(os.path.join(ROOT, "discotoolkit", "*.py")):
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
                public.add(node.name)
    undocumented = sorted(public - documented - INTERNAL)
    assert not undocumented, (
        "not in docs/API.md (add `::: discotoolkit.<Module>.<name>`, or list it as internal in "
        "tests/test_docs.py): %s" % undocumented
    )


def test_api_reference_names_only_things_that_exist():
    api = read("docs/API.md")
    for module, name in re.findall(r"^:::\s+discotoolkit\.(\w+)\.(\w+)", api, re.M):
        source = read("discotoolkit/%s.py" % module)
        assert re.search(r"^(def|class)\s+%s\b" % name, source, re.M), "%s.%s is gone" % (module, name)


def test_tutorials_link_to_pages_not_to_notebook_files_and_not_to_the_v2_site():
    problems = []
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "*.ipynb"))):
        text = "\n".join("".join(c["source"]) for c in json.load(open(path, encoding="utf-8"))["cells"])
        name = os.path.basename(path)
        # a relative link to another .ipynb works on GitHub but is a dead link on the site
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if target.endswith(".ipynb") and not target.startswith("http"):
                problems.append("%s links to the file %s; link to the page on the docs site" % (name, target))
        if "immunesinglecell.org" in text:
            problems.append("%s sends readers to the DISCO V2 site; V1 is the supported server" % name)
    assert not problems, "; ".join(problems)


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
