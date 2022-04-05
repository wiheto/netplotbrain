
## Figures over multiple rows

```python
# Import packages
import netplotbrain
import pandas as pd

# Load example data 
nodes = pd.read_csv('./example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./example_edges.tsv', sep='\t', index_col=0)

# Plot figure
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  nodecolorby='community',
                  view=['LSR', 'AIP'],
                  frames=2)
```

