# %% [markdown]
""" 
# Figures over multiple rows

To plot multiple rows of views, you specify a list of strings specifying the viewing angles. The crucial argument here is:

`view=['LSR', 'AIP'],`

"""

# %%

# Import packages
import netplotbrain
import pandas as pd

# Load example data 
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# Plot figure
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  nodes=nodes,
                  node_size='centrality_measure1',
                  edges=edges,
                  node_color='community',
                  view=['LSR', 'AIP'])

