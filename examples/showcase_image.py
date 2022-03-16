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
                  title='Netplotbrain: plot networks',
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
                  edgewidthscale=0.5)


ax = fig.add_subplot(343, projection='3d')

netplotbrain.plot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['L'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  title='At any viewing angle',
                  fig=fig, ax=ax,
                  edgewidthscale=0.5)


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
                  title='Easily set color and size',
                  fig=fig, ax=ax,
                  nodecmap='gnuplot',
                  edgealpha=0.5,
                  edgewidthscale=0.5,
                  nodescale=10,
                  nodecolorlegend=False,
                  nodesizelegend=False,)


ax = fig.add_subplot(348, projection='3d')

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
                  title='Different brain themes',
                  fig=fig, ax=ax,
                  nodecolorlegend=False,
                  nodesizelegend=False,)

ax = fig.add_subplot(345, projection='3d')

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
                  title='Show one hemisphere',
                  fig=fig, ax=ax,
                  nodecmap='gnuplot',
                  nodecolorlegend=False,
                  nodesizelegend=False,)


ax = fig.add_subplot(3, 4, 6, projection='3d')


edgedf = pd.DataFrame()
edgedf['i'] = [60, 95]
edgedf['j'] = [95, 51]
edgedf['weight'] = [1, 0.75]
nodes_col = np.zeros([100])
nodes_col[95] = 1
nodes_col[[51, 60]] = 2
nodes_seed = pd.DataFrame(data={'seed_roi': nodes_col})
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view='S',
                  nodeimg={'atlas': 'Schaefer2018',
                           'desc': '100Parcels7Networks',
                           'resolution': 1},
                  nodetype='parcels',
                  edges=edgedf,
                  nodes=nodes_seed,
                  templatealpha=0.03,
                  title='Different node styles',
                  templatecolor='gray',
                  highlightnodes=[60, 95, 51],
                  highlightlevel=1,
                  fig=fig, ax=ax,
                  edgewidthscale=3,
                  nodecolorby='seed_roi',
                  edgecolor='darkred',
                  nodecolorlegend=False,
                  nodesizelegend=False,)



ax = fig.add_subplot(3, 4, 7, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view='L',
                  nodes='./examples/example_nodes.tsv',
                  hemisphere=['R'],
                  nodescale=5,
                  edges='./examples/example_edges.tsv',
                  templatealpha=0.05,
                  title='Highlight results',
                  templatecolor='gray',
                  highlightlevel=0.9,
                  highlightnodes=[6, 8, 25, 29],
                  fig=fig, ax=ax,
                  nodecolorlegend=False,
                  nodesizelegend=False,)




ax = fig.add_subplot(349, projection='3d')

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                           'desc': '400Parcels7Networks',
                           'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  title='Plot a parcellation',
                  nodetype='parcels',
                  nodealpha=0.5,
                  nodecolor='Set3',
                  fig=fig, ax=ax)


ax = fig.add_subplot(3, 4, 10, projection='3d')
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
                  title='Community templates',
                  nodecolorlegend=False,
                  nodesizelegend=False,)


ax = fig.add_subplot(3, 4, 11, projection='3d')
netplotbrain.plot(nodes=atlasinfo,
                  nodeimg={'atlas': 'Schaefer2018',
                           'desc': '400Parcels7Networks',
                           'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['S'],
                  nodetype='parcels',
                  nodecmap='Dark2',
                  nodecolorby='yeo7networks',
                  nodealpha = 0.8,
                  title = 'Highlight a community',
                  highlightnodes={'yeo7networks': 'Cont'},
                  highlightlevel=0.95,
                  fig=fig, ax=ax,
                  nodecolorlegend=False,
                  nodesizelegend=False)


ax = fig.add_subplot(3, 4, 12, projection='3d')
nodes_whs = nodes.copy()
nodes_whs['x'] = nodes_whs['x'] / 8
nodes_whs['y'] = nodes_whs['y'] / 8
nodes_whs['z'] = nodes_whs['z'] / 8
netplotbrain.plot(template='WHS',
                  templatestyle='surface',
                  view='S',
                  nodes=nodes_whs,
                  nodesize='centrality_measure1',
                  title='TemplateFlow integration',
                  edges=edges,
                  nodescale=80,
                  templatevoxsize=0.2,
                  fig=fig, ax=ax,
                  edgewidthscale=0.5,
                  nodecolorlegend=False,
                  nodesizelegend=False)

fig.savefig('./examples/figures/showcase.png', dpi=150)

