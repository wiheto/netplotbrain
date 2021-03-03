import numpy as np
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(2021)

n = 10  # number of nodes
m = 20  # number of edges

# CREATE THE NODES
# 8 psudeorandom xyz coordinates
X = np.random.uniform(-50, 50, n)
y = np.random.uniform(-90, 60, n)
z = np.random.uniform(-40, 50, n)
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


# Plot single view
netplotbrain.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view='R',
         nodes=nodesdf,
         nodesize='centrality_measure1',
         edges=edges)
plt.savefig('./examples/figures/singleview.png', dpi=150)


# Plot single view with different size
netplotbrain.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view='R',
         nodes=nodesdf,
         nodesize='centrality_measure2',
         edges=edges)
plt.savefig('./examples/figures/bet1.png', dpi=150)


# Plot multiple rows

netplotbrain.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         nodes=nodesdf,
         nodesize='centrality_measure1',
         edges=edges,
         view=['LSR', 'AIP'])
plt.savefig('./examples/figures/rows1.png', dpi=150)


# Plot different styles

netplotbrain.plot(template='MNI152NLin2009cAsym',
         templatestyle='filled',
         view='R',
         nodes=nodesdf,
         nodesize='centrality_measure1',
         edges=edges)
plt.savefig('./examples/figures/styles1.png', dpi=150)

netplotbrain.plot(template='MNI152NLin2009cAsym', templatestyle='cloudy',
         view='R',
         nodes=nodesdf, nodesize='centrality_measure1',
         edges=edges)
plt.savefig('./examples/figures/styles2.png', dpi=150)

# Plot sequence
netplotbrain.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view='RP',
         nodes=nodesdf, nodesize='centrality_measure1',
         edges=edges, frames=3)
plt.savefig('./examples/figures/seq1.png')

netplotbrain.plot(template='MNI152NLin2009cAsym',
         templatestyle='cloudy',
         view='RP',
         nodes=nodesdf, nodesize='centrality_measure1',
         edges=edges, frames=3)
plt.savefig('./examples/figures/seq2.png')


# Plot on different template
# Rquires slightly different coordinates
# 8 psudeorandom xyz coordinates
# nodex = np.array([-4, -3, 2, 0, 4, -1, 3, 5])
# nodey = np.array([-8, -4, 5, 1, 5, -6, -1, 3])
# nodez = np.array([1, 2, -1, 2, 2, 4, 1, 0])
# Some psuedo_centrality_measure1 measure to demonstrate size
# centrality_measure1 = np.array([0.3, 0.3, 1, 0.15, 0.2, 0.8, 0.4, 0.3])
# nodes = pd.DataFrame(data={'x': nodex, 'y': nodey,
#                           'z': nodez, 'centrality_measure1': centrality_measure1})
# 
# 
# netplotbrain.plot(template='WHS',
#          templatestyle='surface',
#          nodes=nodesdf,
#          nodesize='centrality_measure1',
#          edges=edges,
#          view=['LS'],
#          frames=2,
#          nodescale=0.5,
#          surface_resolution=1)
# plt.savefig('./examples/figures/whs1.png', dpi=150)

# Plot atlas as nodes

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                  'desc': '400Parcels7Networks',
                  'resolution': 1},
         template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view=['LSR'],
         nodetype='circles')
plt.savefig('./examples/figures/atlas_circles.png', dpi=150)

# Plot atlas as parcels

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                  'desc': '400Parcels7Networks',
                  'resolution': 1},
         template='MNI152NLin2009cAsym',
         templatestyle=None,
         view=['LSR'],
         nodetype='parcels',
         nodealpha=0.5,
         nodecolor='Set3')
plt.savefig('./examples/figures/atlas_parcels.png', dpi=150)
