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
2. Commit and push to `main`; wait for the CI checks to pass.
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
