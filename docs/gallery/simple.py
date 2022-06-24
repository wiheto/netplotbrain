# %% [markdown]
""" 
# Simple plot

Below, we load some test data and only specify the template space we would like it plotted in.

"""

#%% 
# Load imports
import netplotbrain
import pandas as pd

# %% 
#Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
# peak at first lines of nodes dataframe
nodes.head()

# %%
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)
# peak at first lines of edges dataframe
edges.head()

# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  nodes=nodes,
                  edges=edges)

