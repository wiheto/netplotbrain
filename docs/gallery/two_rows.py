#  
# # Figures over multiple rows
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/two_rows.ipynb)
#
# To plot multiple rows of views, you specify a list of strings specifying the viewing angles. The crucial argument here is:
#
# `view=['LSR', 'AIP'],`

# +

# Import packages
import netplotbrain
import pandas as pd

#Path to node and edge example data on netplotbrain
nodepath = 'https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/example_nodes.tsv'
edgepath = 'https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/example_edges.tsv'

# Load example data 
nodes = pd.read_csv(nodepath, sep='\t', index_col=0)
edges = pd.read_csv(edgepath, sep='\t', index_col=0)

# Plot figure
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  nodes=nodes,
                  node_size='centrality_measure1',
                  edges=edges,
                  node_color='community',
                  view=['LSR', 'AIP'])

