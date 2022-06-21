# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
# %% Simple single view

import netplotbrain
import pandas as pd

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# Plot single view
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  tempalte='glass',
                  nodes=nodes,
                  nodescale=50,
                  edges=edges)

