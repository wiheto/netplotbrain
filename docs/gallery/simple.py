# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

#  
# # Simple plot
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/simple.ipynb)
# Below, we load some test data and only specify the template space we would like it plotted in.

# Load imports
import netplotbrain
import pandas as pd

#Path to node and edge example data on netplotbrain
nodepath = 'https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/example_nodes.tsv'
edgepath = 'https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/example_edges.tsv'

#Example node and edges dataframes included with package
nodes = pd.read_csv(nodepath, sep='\t', index_col=0)
# peak at first lines of nodes dataframe
nodes.head()

edges = pd.read_csv(edgepath, sep='\t', index_col=0)
# peak at first lines of edges dataframe
edges.head()

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  nodes=nodes,
                  edges=edges)

