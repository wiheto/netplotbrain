# In these examples we demonstrate how different templates

import numpy as np
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(2021)

n = 10  # number of nodes
m = 20  # number of edges

# Different tepmlates have different coordinate systems.
# We generate the same type of data for each.
# But specify the limits in the coordinate system for the random data to be on the brain.
def create_random_data(n, m, xlim, ylim, zlim):
    # CREATE THE NODES
    # 8 psudeorandom xyz coordinates
    X = np.random.uniform(xlim[0], xlim[1], n)
    y = np.random.uniform(ylim[0], ylim[1], n)
    z = np.random.uniform(zlim[0], zlim[1], n)
    # Some random centrality measures to demonstrate size
    centrality_measure1 = np.random.binomial(10, 0.3, n) / 10
    centrality_measure2 = np.random.binomial(10, 0.6, n) / 10
    nodesdf = pd.DataFrame(data={'x': X, 'y': y,
                            'z': z, 'centrality_measure1': centrality_measure1,
                            'centrality_measure2': centrality_measure2})
    ## CREATE THE EDGES.
    # Randomly selet edges
    ind = np.triu_indices(n, k=1)
    eon = np.random.permutation(len(ind[0]))
    edges = np.zeros([n, n])
    # Generate some random wieghts between 0 and 1
    weights = np.random.binomial(10, 0.25, m) / 10
    edges[ind[0][eon[:m]], ind[1][eon[:m]]] = weights
    # Make symetrical
    edges += edges.transpose()
    return nodesdf, edges


# Generate data for OASIS30ANTs
xlim = [-160, -80]
ylim = [-180, -100]
zlim = [-180, -60]
nodes, edges = create_random_data(n, m, xlim, ylim, zlim)

# Plot single view
netplotbrain.plot(template=None,
         template_style=None,
         view='LSR',
         nodes=nodes,
         node_scale=60,
         node_size='centrality_measure1',
         edges=edges)

plt.savefig('./examples/figures/template_oasis30ants.png', dpi=150)

# Generate data for WHS
xlim = [-6, 6]
ylim = [-10, 6]
zlim = [-3, 6]
nodes, edges = create_random_data(n, m, xlim, ylim, zlim)

# Setting template_voxelsize to 0.2 will make it slightly quicker
# Due to the voxel size being smaller, the nodes are currently smaller
# So scaling the nodes is useful.
netplotbrain.plot(template='WHS',
         template_style='surface',
         view='LSR',
         nodes=nodes,
         node_size='centrality_measure1',
         edges=edges,
         node_scale=10,
         template_voxelsize=0.2)

plt.savefig('./examples/figures/template_whs.png', dpi=150)


