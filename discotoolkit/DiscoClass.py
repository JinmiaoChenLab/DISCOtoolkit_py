class Filter:
    def __init__(self, sample = None, project = None, tissue = None, disease = None, platform = None, sample_type = None,
                 cell_type = None, cell_type_confidence = "medium", include_cell_type_children = True, min_cell_per_sample = 100):
        
        # handling for string and list input
        self.sample = self.convert_to_list(sample)
        self.project = self.convert_to_list(project)
        self.tissue = self.convert_to_list(tissue)
        self.disease = self.convert_to_list(disease)
        self.platform = self.convert_to_list(platform)
        self.sample_type = self.convert_to_list(sample_type)
        self.cell_type = self.convert_to_list(cell_type)
        self.cell_type_confidence = cell_type_confidence
        self.include_cell_type_childen = include_cell_type_children
        self.min_cell_per_sample = min_cell_per_sample

    def convert_to_list(self, var):
        if isinstance(var, str):
            return [var]
        else:
            return var

class FilterData:
    def __init__(self, sample_metadata = None, cell_type_metadata = None, sample_count = None, cell_count = None, filter = Filter()):
        self.sample_metadata = sample_metadata
        self.cell_type_metadata = cell_type_metadata
        self.sample_count = sample_count
        self.cell_count = cell_count
        self.filter = filter