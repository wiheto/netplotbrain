#  
# # Template from TemplateFlow: MNIInfant
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/infant.ipynb)
#
# To plot different templtes from templateflow, you just need to change the template specification:
#
# `template='MNIInfant',`
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
nodes_inf = nodes.copy()
nodes_inf['x'] = nodes_inf['x'] / 1.25
nodes_inf['y'] = nodes_inf['y'] / 1.25
nodes_inf['z'] = nodes_inf['z'] / 1.25

# Plot figure
netplotbrain.plot(template='MNIInfant_cohort-2',
         template_style='surface',
         title='Infant template',
         view='LSR',
         nodes=nodes_inf,
         node_size='centrality_measure1',
         node_color='community',
         node_scale=80,
         edges=edges,
         template_voxelsize=5)

