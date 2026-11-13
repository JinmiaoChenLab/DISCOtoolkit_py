"""Exercise the quickstart's numerical dependencies without downloading DISCO data.

UMAP 0.6 stopped copying float32 neighbor distances. Scanpy can pass a sliced neighbor
matrix, and UMAP's Numba kernel then rejects its non-contiguous memory layout.

    python tests/test_embedding.py
"""
import unittest

import numpy as np
import scanpy as sc
from anndata import AnnData
from scipy import sparse
from umap.umap_ import fuzzy_simplicial_set


class EmbeddingTests(unittest.TestCase):
    def test_neighbor_graph_accepts_strided_float32_distances(self):
        n_cells, n_neighbors = 32, 5
        # Search backends may return an extra neighbor; Scanpy slices it off.
        indices = (np.arange(n_cells)[:, None] + np.arange(n_neighbors + 1)) % n_cells
        distances = np.tile(np.arange(n_neighbors + 1, dtype=np.float32), (n_cells, 1))
        indices, distances = indices[:, :n_neighbors], distances[:, :n_neighbors]
        self.assertFalse(distances.flags.c_contiguous)

        graph, _, _ = fuzzy_simplicial_set(
            sparse.coo_matrix((n_cells, 1)), n_neighbors, np.random.RandomState(0),
            "euclidean", knn_indices=indices, knn_dists=distances,
        )
        self.assertEqual(graph.shape, (n_cells, n_cells))
        self.assertGreater(graph.nnz, 0)
        self.assertTrue(np.isfinite(graph.data).all())
        self.assertTrue(((graph.data >= 0) & (graph.data <= 1)).all())
        self.assertEqual((graph.tocsr() - graph.T.tocsr()).nnz, 0)

    def test_quickstart_preprocessing_and_umap(self):
        adata = AnnData(np.random.default_rng(42).poisson(2, size=(120, 80)).astype(np.float32))
        sc.pp.filter_genes(adata, min_cells=10)
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)
        sc.pp.highly_variable_genes(adata, n_top_genes=50)
        sc.pp.pca(adata, mask_var="highly_variable")
        sc.pp.neighbors(adata)
        sc.tl.umap(adata, random_state=0)

        self.assertEqual(adata.obsm["X_umap"].shape, (adata.n_obs, 2))
        self.assertTrue(np.isfinite(adata.obsm["X_umap"]).all())
        self.assertGreater(adata.obsp["connectivities"].nnz, 0)


if __name__ == "__main__":
    unittest.main()
