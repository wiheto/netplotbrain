#  
# # Template from TemplateFlow: WHS
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/whs.ipynb)
#
# To plot different templtes from templateflow, you just need to change the template specification:
#
# `template='WHS',`
#
# The example nodes are scaled as the template is smalled than regular MNI space.

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

# Rescale example node data to fit template
nodes_whs = nodes.copy()
nodes_whs['x'] = nodes_whs['x'] / 8
nodes_whs['y'] = nodes_whs['y'] / 8
nodes_whs['z'] = nodes_whs['z'] / 8

# Plot figure
netplotbrain.plot(template='WHS',
         template_style='surface',
         title='Multiple templates possible',
         view='LSR',
         nodes=nodes_whs,
         node_size='centrality_measure1',
         edges=edges,
         node_color='community',
         node_scale=80,
         template_voxelsize=0.2)
