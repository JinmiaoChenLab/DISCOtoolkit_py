"""
Class for filtering dataset
"""

class Filter:
    """
    Filter class object to save the attributes for filtering the dataset from DISCO

    sample                      String    e.g. GSM3891625_3;
    project                     String;
    tissue                      String    e.g. Lung, Bladder;
    disease                     String    e.g. PDAC;
    platform                    String    e.g. 10x3';
    sample_type                 String;
    cell_type                   String;
    cell_type_confidence        String    e.g. high;
    include_cell_type_children  Bool      e.g. True;
    min_cell_per_sample         Int       e.g. 300;

    return Class object
    """

    def __init__(self, sample = None, project = None, tissue = None, disease = None, platform = None, sample_type = None,
                 cell_type = None, cell_type_confidence : str = "medium", include_cell_type_children : bool = True, min_cell_per_sample : int = 100):
        
        # handling for string and list input
        self.sample = self.convert_to_list(sample) # sample id
        self.project = self.convert_to_list(project) # project, lab, or dataset from different author
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

    """
    Wrapper class on top of the Filter object to get dataset's summary such as cell count and sample count and the metadata
    """
    def __init__(self, sample_metadata = None, cell_type_metadata = None, sample_count = None, cell_count = None, filter = Filter()):
        self.sample_metadata = sample_metadata
        self.cell_type_metadata = cell_type_metadata
        self.sample_count = sample_count
        self.cell_count = cell_count
        self.filter = filter