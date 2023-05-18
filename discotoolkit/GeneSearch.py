import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# import variable and class from other script
from .GlobalVariable import logging, prefix_disco_url
from .DiscoClass import FilterData, Filter
from .GetMetadata import check_in_list


def plot_gene(gene: str = "IGKC"):
    url = f"https://www.immunesinglecell.org/api/vishuo/geneExp/getRefExp?gene={gene}"
    response = requests.get(url)
    data = response.json()[:8]

    # Extract relevant information from JSON data
    expression_values = []
    cell_types = []
    tissues = []
    combined = []

    for entry in data:
        expression_values.append([float(val) for val in entry[0].split(";") if val])
        cell_types.append(entry[1])
        tissues.append(entry[3])
        combined.append(cell_types + tissues)

    # Create a list of dataframe
    df = pd.DataFrame({"Expression": expression_values, "Cell Type": cell_types, "Tissue": tissues})

    # # Set the figure size
    # plt.figure(figsize=(12, 8))

    # # Create grouped violin plot using stripplot
    # ax = sns.stripplot(data=df, x="Cell Type", y="Expression", hue="Tissue", jitter=True, dodge=True)

    # # Customize the plot
    # ax.legend(title="Tissue")
    # ax.set_title(f"Gene Expression Grouped Violin Plot ({gene})")
    # ax.set_xlabel("Cell Type")
    # ax.set_ylabel("Expression")

    # # Rotate x-axis tick labels
    # plt.xticks(rotation=45, ha='right')

    # # Adjust spacing between x-axis labels to avoid overlapping
    # plt.tight_layout()

    # # Display the plot
    # plt.show()


    return None