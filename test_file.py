# first import the installed package
import discotoolkit as dt

# filtering the sample based on the metadata
filter = dt.Filter(
    sample = "AML003_3p",
    cell_type="CD16 monocyte"
)

# apply the filter of interest
metadata = dt.filter_disco_metadata(filter)

# download data to the local directory
download_log = dt.download_disco_data(metadata, output_dir = "disco_data")