import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Union
import colorcet as cc


def gene_search(gene : str, atlas : Union[str, list] = None, figsize : tuple = None, dpi : int = 300):

    """Function to search for the gene expression level the same as the input gene search bar in DISCO website.

    Args:
        gene (String): name of the gene in capital letter. e.g. LYVE1.
        atlas (String or List of String, Optional): User defined atlas for visualisation. Default to None to search for all Atlases.
        figsize (tuple, Optional): Size of the generated figure in tuple. Default to None.
        dpi (int, Optional): DPI resolution for the figure. Default to 300.

    Returns:
        None: This function does not return anything beside plotting
    """

    # condition to handle both the string and list of string of user input for the atlas
    if isinstance(atlas, str):
        atlas = [atlas]

    # url to get the API data
    url = "https://www.immunesinglecell.org/api/vishuo/geneExp/getRefExp?gene=%s" % (gene)
    response = requests.get(url)
    data = response.json()

    # Extract relevant information from JSON data
    expression_values = []
    cell_types = []
    tissues = []
    combined = []
    median_val = []

    # parse the data from json data structure
    for entry in data:
        expression_values.append(np.array([float(val) for val in entry[0].split(";") if val]))
        cell_types.append(entry[1])
        tissues.append(entry[3])
        combined.append(entry[1] + "_"+ entry[3])
        median_val.append(np.median(np.array([float(val) for val in entry[0].split(";") if val])))

    # Store in the dataframe and then melt the numpy array into row
    sample_df = pd.DataFrame({"value": expression_values, "cell types": combined, "atlases": tissues, "median": median_val})
    sample_df = sample_df.sort_values(["median"], ascending=False)
    sample_df = sample_df.explode("value")
    sample_df["value"] = sample_df["value"].astype(float)

    # we add another parameters in case the user want to see from a few selected atlases only
    if atlas is not None:
        sample_df = sample_df[sample_df["atlases"].isin(atlas)].copy()

    # Define the colorcet paletteasdasd
    custom_palette = cc.glasbey_hv

    # saturation for the plot color
    saturation=0.8

    # Set DPI for plotting
    sns.set(rc={'figure.dpi': dpi})

    # setting plot style
    sns.set_style('whitegrid')  # Set the plot style

    # changing the plot size
    if figsize is None:
        fig_len = int(len(set(sample_df["cell types"])))
        fig_height = 8

        figsize = (fig_len, fig_height)

    fig = plt.figure(figsize=figsize)

    # Create the violin plot with different colors based on the 'Category' variable and adding boxplot to assist user with median value
    ax = sns.violinplot(data=sample_df, x='cell types', y='value', hue="atlases", width=0.8, dodge=False, cut=1, saturation = saturation,  plot_kws={'alpha':0.1},
                        inner=None, linewidth=0.0, palette=custom_palette)

    ax_2 = sns.boxplot(x='cell types', y='value', hue="atlases", data=sample_df, palette=custom_palette, dodge=False, width=0.5, saturation = saturation, 
                boxprops={'zorder': 1}, ax=ax)

    # adding rotation to the x axis
    plt.xticks(rotation=-60, ha='left')

    # Remove the duplicated legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:len(handles)//2], labels[:len(labels)//2], title='Atlases', loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol = len(set(tissues)))

    # Removing the atlas string from the x axis
    old_label = ax.get_xticklabels()
    new_label = []
    for each in old_label:
        new_label.append(each.get_text().split("_")[0])
    ax.set_xticklabels(new_label)

    # Remove the top and right spines for aesthetic 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adding the tick to the x axis
    plt.tick_params(axis='x', bottom = True)

    # plt.setp(ax.collections, alpha=.3)
    plt.setp(ax_2.collections, alpha=.5)

    # Set labels and title
    plt.xlabel('Cell Types')
    plt.ylabel('Expression Value')
    plt.title(gene, fontweight='bold')

    # Show the plot
    plt.show()

    return None