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
# Below, we load some test data and only specify the template space we would like it plotted in.
# [Open example in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/simple.ipynb)

# Load imports
import netplotbrain
import pandas as pd
import os

# make sure we are running from 
os.chdir(netplotbrain.__path__[0])

#Example node and edges dataframes included with package
nodes = pd.read_csv('../examples/example_nodes.tsv', sep='\t', index_col=0)
# peak at first lines of nodes dataframe
nodes.head()

edges = pd.read_csv('../examples/example_edges.tsv', sep='\t', index_col=0)
# peak at first lines of edges dataframe
edges.head()

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  nodes=nodes,
                  edges=edges)

