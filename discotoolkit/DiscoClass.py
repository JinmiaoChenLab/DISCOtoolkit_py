"""
Class for filtering dataset
"""

class Filter:
    """Which DISCO samples and cells to look for.

    Every argument is optional; a filter with none of them matches everything. Give a string or a
    list of strings. The list of values each field accepts is `list_metadata_item(field)`.

    Args:
        sample_id (str or list, optional): sample identifier, e.g. "ERX2757110".
        project_id (str or list, optional): project (a study or dataset), e.g. "GSE147520".
        tissue (str or list, optional): e.g. "lung", "bladder".
        disease (str or list, optional): e.g. "COVID-19".
        platform (str or list, optional): sequencing platform, e.g. "10x3'".
        sample_type (str or list, optional): e.g. "control".
        cell_type (str or list, optional): keep samples that contain these cell types, and download
            only those cells.
        cell_type_confidence (str): how sure DISCO's annotation must be: "high", "medium" or "all".
            Defaults to "medium".
        include_cell_type_children (bool): also match the more specific cell types under
            `cell_type`. Defaults to True.
        min_cell_per_sample (int): drop samples with fewer matching cells than this. Defaults to 100.
    """

    def __init__(self, sample_id = None, project_id = None, tissue = None, disease = None, platform = None, sample_type = None,
                 cell_type = None, cell_type_confidence : str = "medium", include_cell_type_children : bool = True, min_cell_per_sample : int = 100):
        
        # handling for string and list input
        self.sample_id = self.convert_to_list(sample_id) # sample id
        self.project_id = self.convert_to_list(project_id) # project, lab, or dataset from different author
        self.tissue = self.convert_to_list(tissue) # organ tissue 
        self.disease = self.convert_to_list(disease) # cancer or non cancer, or COVID-1e9 disease
        self.platform = self.convert_to_list(platform) # sequencing platform
        self.sample_type = self.convert_to_list(sample_type) # type of the sample
        self.cell_type = self.convert_to_list(cell_type) # cell type
        self.cell_type_confidence = cell_type_confidence # cell type annotation confidence
        self.include_cell_type_childen = include_cell_type_children # sub cell type of the broad cell type
        self.min_cell_per_sample = min_cell_per_sample # filter to include the rare cell type

    def convert_to_list(self, var):
        if isinstance(var, str):
            return [var]
        else:
            return var

class FilterData:    

    """The result of a filter: the matching samples, with their counts.

    Returned by `filter_disco_metadata` and passed to `download_disco_data`.

    Attributes:
        sample_metadata (pandas.DataFrame): one row per matching sample.
        cell_type_metadata (pandas.DataFrame): the cell types found in each sample.
        sample_count (int): number of matching samples.
        cell_count (int): number of matching cells.
        filter (Filter): the filter that produced this result.
    """
    def __init__(self, sample_metadata = None, cell_type_metadata = None, sample_count = None, cell_count = None, filter = Filter()):
        self.sample_metadata = sample_metadata
        self.cell_type_metadata = cell_type_metadata
        self.sample_count = sample_count
        self.cell_count = cell_count
        self.filter = filter