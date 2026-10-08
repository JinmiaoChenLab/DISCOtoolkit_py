# Changelog

## 1.3.0 (2026-10-08)

The toolkit is for DISCO V1 only.

- **Removed** the `"v2"` server preset. The toolkit was never tested against DISCO V2, which has its
  own R package (DISCOtoolkit). `set_server("v2")`, or `DISCO_API_URL=v2`, now stops with an error
  that points there instead of quietly using an untested server. A URL can still be given for a
  mirror or a test copy of DISCO V1.
- **Tests** `list_all_columns`, the last public function nothing exercised, has a test and a step in
  the download tutorial.
- **Checks** a new "User check" installs the PyPI release inside the quickstart notebook on a clean
  machine and runs every cell against the public site, as a Colab user would: weekly and after each
  release.

## 1.2.2 (2026-10-08)

Documentation and release housekeeping; no change to how the package behaves.

- **Docs** recommend DISCO V1 as the supported server: the toolkit is developed and tested against
  it. Pointing it at DISCO V2 is possible but untested (`set_server` docstring, README, docs).
- **Docs** fixed three dead links in the quickstart, and the tutorials no longer send readers to the
  DISCO V2 website.
- **Docs** the old Read the Docs site now redirects every page to the new documentation.
- **Releases** each version tag now also gets a GitHub Release, with its notes from this changelog.

## 1.2.1 (2026-10-08)

Fixes for installs on current library versions, and safer reference downloads.

- **Fixed** `CELLiD_cluster` crashing with `KeyError: 0` on pandas 3 (an integer lookup on a
  string-indexed Series).
- **Fixed** `gene_search` crashing on current seaborn and matplotlib (an invalid `plot_kws`
  argument); the title no longer overlaps the legend.
- **Changed** the CELLiD reference tables (`CELLiD_cluster`, `get_atlas`) are downloaded as plain
  CSV, gzip-compressed on the wire, instead of pickles: reading a pickle that came over the network
  can run code. A copy saved by an earlier version is still used, and a server that has no CSV falls
  back to the pickle with a warning.
- **Added** documentation on the DISCO site, with every tutorial re-run against the database on each
  change and the API reference generated from the docstrings:
  https://disco.bii.a-star.edu.sg/v1/docs/toolkit/guide/
- **Added** return type annotations and clearer docstrings (`Filter`, `FilterData`,
  `filter_disco_metadata`, `download_disco_data`).

## 1.2.0

- DISCO V1 is the default server; `set_server("v1" | "v2" | url)` and `DISCO_API_URL` choose another.
- The gene set reference is read as CSV rather than a pickle.
- Python 3.9 or newer; Colab quickstart; PyPI publishing by GitHub Actions (Trusted Publishing).
