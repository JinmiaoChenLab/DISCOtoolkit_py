"""
Does a DISCO server answer everything discotoolkit needs?

Needs only `requests`, so it runs anywhere -- including a fresh Colab notebook:

    !pip install requests
    !python tests/test_server_contract.py                                # DISCO v1 (default)
    !python tests/test_server_contract.py https://immunesinglecell.org/disco_v3_api/   # another server

or with pytest:  DISCO_API_URL=<api root> pytest tests/test_server_contract.py

It checks status codes and the *shape* of each response (the columns and file types the
toolkit reads), not the science. Large reference files are only sampled (first bytes), never
downloaded in full.
"""
import os
import sys

import requests

DEFAULT = "https://disco.bii.a-star.edu.sg/disco_v3_api/"
BASE = (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else os.environ.get("DISCO_API_URL", DEFAULT)).rstrip("/") + "/"
TIMEOUT = 120


def url(path):
    return BASE + path.lstrip("/")


def first_lines(path, n=3, **params):
    """First n text lines of a (possibly huge) response, without downloading the rest."""
    with requests.get(url(path), params=params, stream=True, timeout=TIMEOUT) as r:
        assert r.status_code == 200, "HTTP %s for %s" % (r.status_code, path)
        # Downloads are served as application/octet-stream, which has no charset, so without
        # this requests would hand back bytes instead of text.
        r.encoding = "utf-8"
        lines = []
        for line in r.iter_lines(decode_unicode=True):
            lines.append(line)
            if len(lines) >= n:
                break
        return lines


def first_bytes(path, n=8, **params):
    with requests.get(url(path), params=params, stream=True, timeout=TIMEOUT) as r:
        assert r.status_code == 200, "HTTP %s for %s" % (r.status_code, path)
        size = r.headers.get("Content-Length")
        return next(r.iter_content(chunk_size=n)), (int(size) if size else None)


def columns(line):
    return line.split("\t")


# ---- metadata the Filter / FilterData classes work on ------------------------------------

def test_sample_metadata_has_the_filter_columns():
    header, row = first_lines("toolkit/getSampleMetadata", 2)
    need = {"sample_id", "project_id", "sample_type", "tissue", "disease", "platform", "cell_number"}
    missing = need - set(columns(header))
    assert not missing, "getSampleMetadata lacks columns: %s" % sorted(missing)
    assert len(columns(row)) == len(columns(header)), "rows are not tab-aligned with the header"


def test_cell_type_summary_columns():
    header, row = first_lines("toolkit/getCellTypeSummary", 2)
    assert columns(header) == ["sample_id", "cell_type", "cell_type_score", "cell_number"], columns(header)
    float(columns(row)[2]); int(columns(row)[3])


def test_cell_ontology_is_a_list_of_cell_name_and_parent():
    r = requests.get(url("toolkit/getCellOntology"), timeout=TIMEOUT)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) > 100
    assert {"cell_name", "parent"} <= set(data[0]), data[0]


# ---- per-sample download (download_disco_data) ---------------------------------------------

def _a_sample():
    header, row = first_lines("toolkit/getSampleMetadata", 2)
    cols = columns(header)
    values = columns(row)
    return values[cols.index("project_id")], values[cols.index("sample_id")]


def test_cell_type_labels_for_one_sample():
    project, sample = _a_sample()
    header, row = first_lines("toolkit/getCellTypeSample", 2, sampleId=sample)
    cols = columns(header)
    # the toolkit reads columns 0, 2 and 5 by position, so their order matters
    assert cols[0] == "cell_id" and cols[2] == "cell_type" and cols[5] == "cell_type_score", cols


def test_raw_10x_h5_is_downloadable_and_is_hdf5():
    project, sample = _a_sample()
    head, size = first_bytes("download/getRawH5/%s/%s" % (project, sample))
    assert head.startswith(b"\x89HDF"), "not an HDF5 file: %r" % head
    assert size is None or size > 1000


# ---- CELLiD / scEnrichment reference data ---------------------------------------------------

def test_cellid_reference_is_a_gzip_pickle():
    head, size = first_bytes("toolkit/getRef", type="pkl")
    assert head[:2] == b"\x1f\x8b", "getRef is not gzip data: %r" % head
    assert size is None or size > 1_000_000


def test_cellid_deg_reference_is_a_gzip_pickle():
    head, size = first_bytes("toolkit/getRefDeg", type="pkl")
    assert head[:2] == b"\x1f\x8b", "getRefDeg is not gzip data: %r" % head


def test_gene_set_reference_is_available_as_plain_csv():
    header, row = first_lines("toolkit/getGeneSet", 2, format="csv")
    cols = [c.strip('"') for c in header.split(",")]
    assert cols == ["logfc", "gene", "atlas", "name"], cols


# ---- gene_search ------------------------------------------------------------------------------

def test_gene_reference_expression_rows_have_the_shape_gene_search_reads():
    r = requests.get(url("geneExp/getRefExp"), params={"gene": "CD4"}, timeout=TIMEOUT)
    assert r.status_code == 200
    rows = r.json()
    assert rows, "no reference expression for CD4"
    # entry[0] ';'-separated values, entry[1] cell type, entry[3] atlas / tissue
    assert isinstance(rows[0][0], str) and ";" in rows[0][0]
    assert isinstance(rows[0][1], str) and isinstance(rows[0][3], str)


# ---- housekeeping ---------------------------------------------------------------------------------

def test_server_reports_a_toolkit_version_and_api_url():
    v = requests.get(url("getToolkitVersion"), timeout=TIMEOUT).json()
    assert v.get("version"), v
    u = requests.get(url("getToolkitUrl"), timeout=TIMEOUT).json()
    assert u.get("url", "").startswith("http"), u


def _run_all():
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    print("DISCO toolkit contract test against %s\n" % BASE)
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("  PASS  %s" % name)
        except Exception as error:   # report every failure, do not stop at the first
            failed += 1
            print("  FAIL  %s\n          %s: %s" % (name, type(error).__name__, error))
    print("\n%d/%d passed" % (len(tests) - failed, len(tests)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_all())
