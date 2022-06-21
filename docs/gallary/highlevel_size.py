# %% [markdown]
""" 
# Node properties: size

Netplotbrain allows for specifying different figure properties by only specifyign the column name.

Below we demonstrate how nodesize can change based on different columns in the nodes dataframe.

The key lines of code here are when:

`nodesize='centrality_measure1'`

and

`nodesize='centrality_measure2'`

These columns could be called anything such as "module_degree_zscore" or "efficiency"

"""

# %%  
# Import packages
import netplotbrain
import pandas as pd

# Load example data 
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)
nodes.head()

# %%    
fig = plt.figure()
ax_m2 = fig.add_subplot(121, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  fig = fig,
                  ax = ax_m2,
                  view='A',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  nodecolor='red',
                  edges=edges)

ax_m2 = fig.add_subplot(122, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  fig = fig,
                  ax = ax_m2,
                  view='A',
                  nodes=nodes,
                  nodesize='centrality_measure2',
                  nodecolor='blue',
                  edges=edges)
plt.show()
