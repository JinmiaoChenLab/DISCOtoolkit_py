# Changelog

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
