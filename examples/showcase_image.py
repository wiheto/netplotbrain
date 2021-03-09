# In these examples we demonstrate how different templates 

import numpy as np
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt
import templateflow.api as tf

nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)


fig  = plt.figure()

ax = fig.add_subplot(341, projection='3d')
netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  title='Plot networks',
                  edgeweights='weight',
                  edgealpha=0.5,
                  fig=fig, ax=ax)

ax = fig.add_subplot(342, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['S'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  title='Onto brains',
                  fig=fig, ax=ax,
                  edgescale=0.5)


ax = fig.add_subplot(343, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['L'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  title='Multiple viewing angle',
                  fig=fig, ax=ax,
                  edgescale=0.5)


ax = fig.add_subplot(344, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['A'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolorby='community',
                  nodesize='centrality_measure2',
                  title='Let columns set\ncolor + size',
                  fig=fig, ax=ax,
                  nodecmap='gnuplot',
                  edgealpha=0.5,
                  edgescale=0.5)





ax = fig.add_subplot(345, projection='3d')

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                           'desc': '400Parcels7Networks',
                           'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  title='Show parcellations',
                  nodetype='parcels',
                  nodealpha=0.5,
                  nodecolor='Set3',
                  fig=fig, ax=ax)

ax = fig.add_subplot(346, projection='3d')

netplotbrain.plot(template='WHS',
                  templatestyle='surface',
                  view='S',
                  nodes=nodes / 8,
                  nodesize='centrality_measure1',
                  title='Different brain templates',
                  edges=edges,
                  nodescale=80,
                  templatevoxsize=0.2,
                  fig=fig, ax=ax,
                  edgescale=0.5)



ax = fig.add_subplot(347, projection='3d')

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
                  title='Different themes',
                  fig=fig, ax=ax)

ax = fig.add_subplot(348, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['S'],
                  hemisphere=['L'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolorby='community',
                  nodesize='centrality_measure2',
                  title='Single hemisphere',
                  fig=fig, ax=ax,
                  nodecmap='gnuplot')



ax = fig.add_subplot(349, projection='3d')
atlasinfo = tf.get(template='MNI152NLin2009cAsym',
       atlas='Schaefer2018',
       desc='400Parcels7Networks',
       extension='.tsv')
atlasinfo = pd.read_csv(atlasinfo, sep='\t')
# Parse the info in to get network names
networks = list(map(lambda x: x.split('_')[2], atlasinfo.name.values))
atlasinfo['yeo7networks'] = networks


netplotbrain.plot(nodes=atlasinfo,
                  nodeimg={'atlas': 'Schaefer2018',
                           'desc': '400Parcels7Networks',
                           'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  nodetype='parcels',
                  nodealpha=1,
                  nodecmap='Dark2',
                  nodecolorby='yeo7networks',
                  fig=fig, ax=ax,
                  title='Show communities')


fig.savefig('./examples/figures/showcase.png', dpi=150)

