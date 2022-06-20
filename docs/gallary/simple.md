## Simple single view

```python
import netplotbrain
import pandas as pd

# Example node and edges dataframes included with package
nodes = pd.read_csv('./example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./example_edges.tsv', sep='\t', index_col=0)

# Plot single view
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view='LSR',
                  nodes=nodes,
                  nodescale=40,
                  nodesize='centrality_measure1',
                  edges=edges,
                  nodecolor='community')

```
