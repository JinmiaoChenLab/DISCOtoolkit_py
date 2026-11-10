"""
CELLiD's correlation step: the matrix calculation that replaced pandarallel must give the numbers pandas'
own pairwise Spearman gives (ties, missing values, constant columns included), and CELLiD_cluster must
annotate a small made-up reference correctly. No network.

    python tests/test_cellid_correlation.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from discotoolkit.CELLiD import CELLiD_cluster, _spearman_matrix  # noqa: E402


def pandas_pairwise(ref: pd.DataFrame, user: pd.DataFrame) -> np.ndarray:
    """What the code did before: one Series.corr(method="spearman") per pair."""
    return np.array([[pd.Series(ref.iloc[:, i].to_numpy()).corr(pd.Series(user.iloc[:, j].to_numpy()), method="spearman")
                      for j in range(user.shape[1])] for i in range(ref.shape[1])])


def same(a, b):
    assert a.shape == b.shape, (a.shape, b.shape)
    assert np.array_equal(np.isnan(a), np.isnan(b)), "NaN positions differ"
    assert np.allclose(a[~np.isnan(a)], b[~np.isnan(b)], atol=1e-12), np.nanmax(np.abs(a - b))


def test_matches_pandas_on_continuous_data():
    rng = np.random.default_rng(1)
    ref = pd.DataFrame(rng.normal(size=(300, 12)))
    user = pd.DataFrame(rng.normal(size=(300, 5)))
    same(_spearman_matrix(ref, user), pandas_pairwise(ref, user))


def test_matches_pandas_with_many_ties_like_expression_data():
    rng = np.random.default_rng(2)
    ref = pd.DataFrame(rng.poisson(0.4, size=(400, 10)).astype(float))
    user = pd.DataFrame(rng.poisson(0.4, size=(400, 4)).astype(float))
    same(_spearman_matrix(ref, user), pandas_pairwise(ref, user))


def test_missing_values_use_pairwise_complete_observations():
    rng = np.random.default_rng(3)
    ref = pd.DataFrame(rng.normal(size=(200, 6)))
    user = pd.DataFrame(rng.normal(size=(200, 3)))
    ref.iloc[5, 2] = np.nan
    user.iloc[17, 1] = np.nan
    same(_spearman_matrix(ref, user), pandas_pairwise(ref, user))


def test_a_constant_column_has_no_correlation():
    rng = np.random.default_rng(4)
    ref = pd.DataFrame(rng.normal(size=(50, 3)))
    ref[1] = 7.0
    user = pd.DataFrame(rng.normal(size=(50, 2)))
    result = _spearman_matrix(ref, user)
    assert np.isnan(result[1]).all() and not np.isnan(result[[0, 2]]).any()


def test_cellid_cluster_annotates_a_small_reference():
    rng = np.random.default_rng(5)
    genes = ["G%d" % i for i in range(300)]
    types = ["B cell--blood", "T cell--blood", "Macrophage--lung", "Fibroblast--lung"]
    ref = pd.DataFrame(rng.poisson(1.0, size=(300, 4)).astype(float), index=genes, columns=types)
    # every cluster is a noisy copy of one reference cell type
    picks = [2, 0, 3]
    user = pd.DataFrame({str(c): ref.iloc[:, t] + rng.normal(0, 0.2, size=300) for c, t in enumerate(picks)}, index=genes)
    deg = pd.DataFrame([(t, g) for t in types for g in genes[:150]], columns=["group", "gene"])
    out = CELLiD_cluster(user, ref_data=ref, ref_deg=deg, n_predict=1, ncores=1)
    assert list(out["predicted_cell_type_1"]) == ["Macrophage", "B cell", "Fibroblast"], out
    assert list(out["source_atlas_1"]) == ["lung", "blood", "lung"], out


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
