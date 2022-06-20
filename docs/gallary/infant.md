## Template from TemplateFlow: MNIInfant

```python
# Import packages
import netplotbrain
import pandas as pd

# Load example data 
nodes = pd.read_csv('./example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./example_edges.tsv', sep='\t', index_col=0)

# Rescale example node data to fit template
nodes_inf = nodes.copy()
nodes_inf['x'] = nodes_inf['x'] / 1.25
nodes_inf['y'] = nodes_inf['y'] / 1.25
nodes_inf['z'] = nodes_inf['z'] / 1.25

# Plot figure
netplotbrain.plot(template='MNIInfant',
         templatestyle='surface',
         title='Infant template',
         view='LSR',
         nodes=nodes_inf,
         nodesize='centrality_measure1',
         nodecolor='community',
         nodescale=80,
         edges=edges,
         templatevoxsize=5)

```

