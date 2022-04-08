## Template from TemplateFlow: WHS

```python
# Import packages
import netplotbrain
import pandas as pd

# Load example data 
nodes = pd.read_csv('./example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./example_edges.tsv', sep='\t', index_col=0)

# Rescale example node data to fit template
nodes_whs = nodes.copy()
nodes_whs['x'] = nodes_whs['x'] / 8
nodes_whs['y'] = nodes_whs['y'] / 8
nodes_whs['z'] = nodes_whs['z'] / 8

# Plot figure
netplotbrain.plot(template='WHS',
         templatestyle='surface',
         title='Multiple templates possible',
         view='LSR',
         nodes=nodes_whs,
         nodesize='centrality_measure1',
         edges=edges,
         nodecolorby='community',
         nodescale=80,
         templatevoxsize=0.2)
         
```
