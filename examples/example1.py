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
nodes = pd.DataFrame(data={'x': nodex, 'y': nodey,
                           'z': nodez, 'centrality': centrality})

n = 8  # number of nodes
m = 12  # number of edges
# Random edges connecting the 8 nodes
ind = np.triu_indices(n, k=1)
eon = np.random.permutation(len(ind[0]))
edges = np.zeros([n, n])
edges[ind[0][eon[:m]], ind[1][eon[:m]]] = 1
edges += edges.transpose()

# Generate weighted edges connecting the nodes
edgesdf = pd.DataFrame()
edges_list = list(zip(*np.where(edges != 0)))
edgesdf["i"], edgesdf["j"] = [i[0]
                              for i in edges_list], [i[1] for i in edges_list]
weights = ['0.608', '0.475', '0.456', '0.578', '0.415', '0.953', '0.204', '0.124', '0.608', '0.394', '0.222',
           '0.178', '0.815', '0.993', '0.199', '0.104', '0.789', '0.233', '0.763', '0.248', '0.195', '0.899', '0.904', '0.424']
edgesdf['weight'] = weights
edges = edgesdf

# Plot single view
nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='cloudy',
         view='R',
         nodes=nodes,
         nodesize='centrality',
         edges=edges)
plt.savefig('./examples/figures/singleview.png', dpi=150)

# Plot different styles

nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='filled',
         view='R',
         nodes=nodes,
         nodesize='centrality',
         edges=edges)
plt.savefig('./examples/figures/styles1.png', dpi=150)

nob.plot(template='MNI152NLin2009cAsym', templatestyle='cloudy',
         view='R',
         nodes=nodes, nodesize='centrality',
         edges=edges)
plt.savefig('./examples/figures/styles2.png', dpi=150)

# Plot sequence
nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view='RP',
         nodes=nodes, nodesize='centrality',
         edges=edges, frames=3)
plt.savefig('./examples/figures/seq1.png')

nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='cloudy',
         view='RP',
         nodes=nodes, nodesize='centrality',
         edges=edges, frames=3)
plt.savefig('./examples/figures/seq2.png')
