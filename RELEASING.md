# Releasing discotoolkit

Releases are published to PyPI by GitHub Actions (`.github/workflows/publish.yml`) when a version
tag is pushed. It uses **Trusted Publishing**: GitHub proves its identity to PyPI directly, so there
is no API token to create, store or leak.

## One-time setup

1. **PyPI.** Log in at pypi.org (2FA on), open the `discotoolkit` project, then
   *Manage -> Publishing -> Add a new publisher -> GitHub*, and enter exactly:

   | field | value |
   |---|---|
   | Owner | `JinmiaoChenLab` |
   | Repository name | `DISCOtoolkit_py` |
   | Workflow name | `publish.yml` |
   | Environment name | `pypi` |

   You must be an owner of the project on PyPI to do this.

2. **GitHub.** In the repository, *Settings -> Environments -> New environment*, name it `pypi`.
   Optionally add yourself under *Required reviewers*: every release then waits for your approval
   before anything is uploaded.

## Every release

1. Change the version in **both** `setup.py` and `discotoolkit/__init__.py` (a test checks they agree).
2. Commit and push to `main`; wait for the CI checks to pass. (The release re-runs them anyway:
   if any test fails, nothing is published.)
3. Tag and push the tag (the tag is the version with a leading `v`):

   ```
   git tag v1.2.0
   git push origin v1.2.0
   ```

4. Watch the run under the repository's *Actions* tab. If you set required reviewers, approve it.
   A minute later the release is at https://pypi.org/project/discotoolkit/.

PyPI never accepts the same version twice. If a release goes wrong, fix it and publish the next
version (1.2.1); do not try to reuse the number.

## If the publish step fails

- *"invalid-publisher"*: the four values in step 1 do not match this repository and workflow exactly.
- *"tag ... does not match package version"*: the version in `setup.py` / `__init__.py` was not
  changed to match the tag.

## Documentation

The documentation has one source, this repository, and is built by `.github/workflows/docs.yml`:

| What | Where it comes from |
|---|---|
| Tutorials (`docs/*.ipynb`) | Run against the live DISCO V1 server on every build, so every page shows what the current code does. Committed notebooks carry **no output** (`python tools/execute_notebooks.py --clear` before committing; `tests/test_docs.py` checks). |
| API reference | Generated from the docstrings. Add a function and a `::: discotoolkit.<Module>.<name>` line in `docs/API.md` (a test fails if you forget). |
| Version | Read from `discotoolkit/__init__.py`; write `{{ version }}` in a page to show it. |

It is published to the `docs-site` branch with [mike](https://github.com/jimporter/mike):

- every push to `main` that touches the code or the docs, and a weekly run, publish **dev**;
- a release publishes its version (e.g. **1.2.1**) and moves the **stable** alias to it. The
  tutorials are run *before* anything is uploaded to PyPI, and a tutorial that fails blocks the
  release; the docs are published after PyPI has the package.

The DISCO website mirrors `docs-site` (every 10 minutes) at
https://disco.bii.a-star.edu.sg/v1/docs/toolkit/guide/, so a change to the package shows up there
without anyone copying anything. Until the first release built this way, **stable** points at dev.

Build it locally (needs the DISCO server, or `DISCO_API_URL=<your server>`):

```
pip install -e . -r requirements-docs.txt
python tools/execute_notebooks.py        # runs every tutorial, in place
mkdocs serve                             # http://127.0.0.1:8000
python tools/execute_notebooks.py --clear   # before committing
```
