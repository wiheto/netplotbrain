import numpy as np
import netonbrain as nob
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(2021)

# 8 psudeorandom xyz coordinates
nodex = np.array([42, -42, -40, 40, 12, -12, -18, 18])
nodey = np.array([-60, -60, 40, 40, 56, 56, -44, -44])
nodez = np.array([30, 30, -16, -16, 35, 35, 44, 44])
# Some psuedo_centrality measure to demonstrate size
centrality = np.array([30, 30, 50, 15, 20, 10, 5, 25])
nodes = pd.DataFrame(data={'x': nodex, 'y': nodey, 'z': nodez, 'centrality': centrality})

n = 8 # number of nodes
m = 12 # number of edges
# Random edges connecting the 8 nodes
ind = np.triu_indices(n, k=1)
eon = np.random.permutation(len(ind[0])) 
edges = np.zeros([n, n])
edges[ind[0][eon[:m]], ind[1][eon[:m]]] = 1
edges += edges.transpose()

### Plot single view
nob.plot(template='MNI152NLin2009cAsym', templatestyle='glass',
                    view='R', 
                    nodes=nodes, nodesize='centrality',
                    edges=edges)
plt.savefig('./examples/figures/singleview.png', dpi=300)

### Plot different styles

nob.plot(template='MNI152NLin2009cAsym', templatestyle='filled',
                    view='R', 
                    nodes=nodes, nodesize='centrality',
                    edges=edges)
plt.savefig('./examples/figures/styles1.png', dpi=300)

nob.plot(template='MNI152NLin2009cAsym', templatestyle='glass',
                    view='R', 
                    nodes=nodes, nodesize='centrality',
                    edges=edges)
plt.savefig('./examples/figures/styles2.png', dpi=300)

### Plot sequence
nob.plot(template='MNI152NLin2009cAsym', templatestyle='glass',
                    view='RP', 
                    nodes=nodes, nodesize='centrality',
                    edges=edges, frames=3)
plt.savefig('./examples/figures/seq1.png')

nob.plot(template='MNI152NLin2009cAsym', templatestyle='filled',
                    view='RP', 
                    nodes=nodes, nodesize='centrality',
                    edges=edges, frames=3)
plt.savefig('./examples/figures/seq2.png')
