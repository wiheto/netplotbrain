# %% [markdown]
""" 
# Template from TemplateFlow: MNIInfant

To plot different templtes from templateflow, you just need to change the template specification:

`template='MNIInfant',`

The example nodes are scaled as the template is smalled than regular MNI space.
"""

# %%
# Import packages
import netplotbrain
import pandas as pd

# Load example data 
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# Rescale example node data to fit template
nodes_inf = nodes.copy()
nodes_inf['x'] = nodes_inf['x'] / 1.25
nodes_inf['y'] = nodes_inf['y'] / 1.25
nodes_inf['z'] = nodes_inf['z'] / 1.25

# Plot figure
netplotbrain.plot(template='MNIInfant_cohort-2',
         templatestyle='surface',
         title='Infant template',
         view='LSR',
         nodes=nodes_inf,
         nodesize='centrality_measure1',
         nodecolor='community',
         nodescale=80,
         edges=edges,
         templatevoxsize=5)

