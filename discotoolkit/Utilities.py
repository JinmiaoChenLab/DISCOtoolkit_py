import h5py
import numpy as np
from scipy.sparse import csr_matrix
from pathlib import Path


def write_10X_h5(adata, file):
    """Writes adata to a 10X-formatted h5 file.

    Note that this function is not fully tested and may not work for all cases.
    It will not write the following keys to the h5 file compared to 10X:
    '_all_tag_keys', 'pattern', 'read', 'sequence'

    Args:
        adata (AnnData object): AnnData object to be written.
        file (str): File name to be written to. If no extension is given, '.h5' is appended.

    Raises:
        FileExistsError: If file already exists.

    Returns:
        None
    """

    if ".h5" not in file:
        file = f"{file}.h5"
    if Path(file).exists():
        raise FileExistsError(f"There already is a file `{file}`.")

    def int_max(x):
        return int(max(np.floor(len(str(int(max(x)))) / 4), 1) * 4)

    def str_max(x):
        return max([len(i) for i in x])

    w = h5py.File(file, "w")
    grp = w.create_group("matrix")
    grp.create_dataset(
        "barcodes",
        data=np.array(adata.obs_names, dtype=f"|S{str_max(adata.obs_names)}"),
    )
    grp.create_dataset(
        "data", data=np.array(adata.X.data, dtype=f"<i{int_max(adata.X.data)}")
    )
    ftrs = grp.create_group("features")
    # this group will lack the following keys:
    # '_all_tag_keys', 'feature_type', 'genome', 'id', 'name', 'pattern', 'read', 'sequence'
    ftrs.create_dataset(
        "feature_type",
        data=np.array(
            adata.var.feature_types, dtype=f"|S{str_max(adata.var.feature_types)}"
        ),
    )
    ftrs.create_dataset(
        "genome",
        data=np.array(adata.var.genome, dtype=f"|S{str_max(adata.var.genome)}"),
    )
    ftrs.create_dataset(
        "id",
        data=np.array(adata.var.gene_ids, dtype=f"|S{str_max(adata.var.gene_ids)}"),
    )
    ftrs.create_dataset(
        "name", data=np.array(adata.var.index, dtype=f"|S{str_max(adata.var.index)}")
    )
    grp.create_dataset(
        "indices", data=np.array(adata.X.indices, dtype=f"<i{int_max(adata.X.indices)}")
    )
    grp.create_dataset(
        "indptr", data=np.array(adata.X.indptr, dtype=f"<i{int_max(adata.X.indptr)}")
    )
    grp.create_dataset(
        "shape",
        data=np.array(list(adata.X.shape)[::-1], dtype=f"<i{int_max(adata.X.shape)}"),
    )
