import numpy as np
import netonbrain as nob
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(2021)

# 8 psudeorandom xyz coordinates
nodex = np.array([42, -42, -40, 40, 12, -12, -18, 18])
nodey = np.array([-60, -60, 40, 40, 56, 56, -44, -44])
nodez = np.array([30, 30, -16, -16, 35, 35, 44, 44])
# Some psuedo_strength measure to demonstrate size
strength = np.array([0.3, 0.3, 1, 0.15, 0.2, 0.8, 0.4, 0.3])
betweenness = np.array([1, 0.1, 1, 1, 0.5, 0.4, 0.9, 1])
communities = np.array([1, 1, 5, 5, 5, 7, 7, 8])
nodesdf = pd.DataFrame(data={'x': nodex, 'y': nodey,
                           'z': nodez, 'strength': strength,
                           'betweenness': betweenness,
                           'communities': communities})

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
         templatestyle='surface',
         view='R',
         nodes=nodesdf,
         nodesize='strength',
         edges=edges)
plt.savefig('./examples/figures/singleview.png', dpi=150)


# Plot single view with different size
nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view='R',
         nodes=nodesdf,
         nodesize='betweenness',
         edges=edges)
plt.savefig('./examples/figures/bet1.png', dpi=150)


# Plot multiple rows

nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         nodes=nodesdf,
         nodesize='strength',
         edges=edges,
         view=['LSR', 'AIP'])
plt.savefig('./examples/figures/rows1.png', dpi=150)


# Plot different styles

nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='filled',
         view='R',
         nodes=nodesdf,
         nodesize='strength',
         edges=edges)
plt.savefig('./examples/figures/styles1.png', dpi=150)

nob.plot(template='MNI152NLin2009cAsym', templatestyle='cloudy',
         view='R',
         nodes=nodesdf, nodesize='strength',
         edges=edges)
plt.savefig('./examples/figures/styles2.png', dpi=150)

# Plot sequence
nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view='RP',
         nodes=nodesdf, nodesize='strength',
         edges=edges, frames=3)
plt.savefig('./examples/figures/seq1.png')

nob.plot(template='MNI152NLin2009cAsym',
         templatestyle='cloudy',
         view='RP',
         nodes=nodesdf, nodesize='strength',
         edges=edges, frames=3)
plt.savefig('./examples/figures/seq2.png')


# Plot on different template
# Rquires slightly different coordinates
# 8 psudeorandom xyz coordinates
# nodex = np.array([-4, -3, 2, 0, 4, -1, 3, 5])
# nodey = np.array([-8, -4, 5, 1, 5, -6, -1, 3])
# nodez = np.array([1, 2, -1, 2, 2, 4, 1, 0])
# Some psuedo_strength measure to demonstrate size
# strength = np.array([0.3, 0.3, 1, 0.15, 0.2, 0.8, 0.4, 0.3])
# nodes = pd.DataFrame(data={'x': nodex, 'y': nodey,
#                           'z': nodez, 'strength': strength})
# 
# 
# nob.plot(template='WHS',
#          templatestyle='surface',
#          nodes=nodesdf,
#          nodesize='strength',
#          edges=edges,
#          view=['LS'],
#          frames=2,
#          nodescale=0.5,
#          surface_resolution=1)
# plt.savefig('./examples/figures/whs1.png', dpi=150)

# Plot atlas as nodes

nob.plot(nodeimg={'atlas': 'Schaefer2018',
                  'desc': '400Parcels7Networks',
                  'resolution': 1},
         template='MNI152NLin2009cAsym',
         templatestyle='surface',
         view=['LSR'],
         nodetype='circles')
plt.savefig('./examples/figures/atlas_circles.png', dpi=150)

# Plot atlas as parcels

nob.plot(nodeimg={'atlas': 'Schaefer2018',
                  'desc': '400Parcels7Networks',
                  'resolution': 1},
         template='MNI152NLin2009cAsym',
         templatestyle=None,
         view=['LSR'],
         nodetype='parcels',
         nodealpha=0.5,
         nodecolor='Set3')
plt.savefig('./examples/figures/atlas_parcels.png', dpi=150)
