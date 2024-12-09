# + [markdown]
"""
# Tutorial 3: The connectivity matrix 

Viewing the connectivity matrix is another way of examining the networks within the brain, complementing other methods. 

In these visualizations a node x node matrix shows the connectivity values. 

To view a connectivity matrix for your nextwork, simply set a view argument to "c".

NetPlotBrain enables you to effortlessly generate a connectivity matrix alongside the brain, along with a few extra features.
"""

# + [markdown]
""" 
## Generating data

So let us generate some normally distributed data to use as our connectivity matrix.
"""

# + 
import numpy as np
import itertools
import pandas as pd
import netplotbrain

# +
mu = np.zeros(30)
sigma = np.eye(30)
# Set within network connectivity
i, j = list(zip(*itertools.combinations(np.arange(0, 10), 2)))
sigma[i, j] = 0.7
i, j = list(zip(*itertools.combinations(np.arange(10, 20), 2)))
sigma[i, j] = 0.7
i, j = list(zip(*itertools.combinations(np.arange(20, 30), 2)))
sigma[i, j] = 0.6
# Set between network connectivity
sigma[20:][:, :20] = -0.2
sigma[10:20][:, :10] = 0.1
sigma = sigma + sigma.T
np.fill_diagonal(sigma, 1)
# Generate the random data
np.random.seed(42)
data = np.random.multivariate_normal(mu, sigma, 1000)

# + 
# Create connectivity matrix
cm = pd.DataFrame(data).corr().values
# Here we see we have created a 30 x 30 matrix
cm.shape

# +
# Plot the connectivity matrix
netplotbrain.plot(edges=cm,
                  view='c')

# + [markdown]
""" 
## Shuffling up the order

Now multiple different options can be specified.
One such opttion is the order of the nodes. Here the nodes are already ordered, but this is not always the case.
"""

# +
random_order = np.random.permutation(np.arange(30))
cm = cm[random_order][:, random_order]
netplotbrain.plot(edges=cm, view='c')

## + [markdown]
# ### cm_order can set the order of nodes. 

# + 
# cm_order is either a list of indicies or a list of communities
cm_order = np.argsort(random_order)
netplotbrain.plot(edges=cm, view='c', 
                  cm_order=cm_order)

## + [markdown]
# ### Turning of the rotated option

# + 
netplotbrain.plot(edges=cm, view='c', 
                  cm_order=cm_order, 
                  cm_rotate=False)

## + [markdown]
# ### ringing in the community with node_color. 

# + 
# Lets put cm back in its correct order
cm = cm[cm_order][:, cm_order]

# Load example nodes, take only xyz and first 30 rows
nodes = pd.read_csv(netplotbrain.__path__[0] + '/example_data/example_nodes.tsv', sep='\t', index_col=0)
nodes = nodes[['x', 'y', 'z']].iloc[:30]
# Add new community names
nodes['community_names'] = ['FP']*10 + ['SM']*10 + ['DMN']*10

# + 
netplotbrain.plot(edges=cm, view='Sc', 
                  nodes=nodes, node_color='community_names', 
                  node_scale=50,
                  node_cmap='Set2',
                  title='Brain and connectivity mastrix sharing colors',
                  subtitles=None,
                  cm_boundarywidth=4,
                  cm_bordercolor = 'black',
                  cm_borderwidth = 2,
                  edge_color='lightgray',
                  edge_wights=0.1)

# + [markdown]
""" 
The above plot also shows the cm_boundarywidth argument which plots the width of the squares associated with node_color.
It also show cm_borderwidth and cm_bordercolor which are the outside boundaries. 
"""
