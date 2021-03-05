# In these examples we demonstrate how different templates 

import numpy as np
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt

nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)


fig  = plt.figure()

ax = fig.add_subplot(331, projection='3d')
netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  fig=fig, ax=ax)

ax = fig.add_subplot(332, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['S'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  fig=fig, ax=ax)


ax = fig.add_subplot(333, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['L'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  fig=fig, ax=ax)





ax = fig.add_subplot(334, projection='3d')

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                           'desc': '400Parcels7Networks',
                           'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  nodetype='parcels',
                  nodealpha=0.5,
                  nodecolor='Set3',
                  fig=fig, ax=ax)

ax = fig.add_subplot(335, projection='3d')

netplotbrain.plot(template='WHS',
                  templatestyle='surface',
                  view='S',
                  nodes=nodes / 8,
                  nodesize='centrality_measure1',
                  edges=edges,
                  nodescale=80,
                  templatevoxsize=0.2,
                  fig=fig, ax=ax)



ax = fig.add_subplot(336, projection='3d')

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='cloudy',
                  view='L',
                  nodes=nodes,
                  hemisphere='R',
                  nodesize='centrality_measure1',
                  edges=edges,
                  templatevoxsize=2,
                  templatealpha=0.025,
                  templatecolor='darkkhaki',
                  fig=fig, ax=ax)


fig.savefig('./examples/figures/showcase.png', dpi=150)