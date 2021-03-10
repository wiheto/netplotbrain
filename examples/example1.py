#%% md
"""
## The basics. 
# This notebook goes through a showcase of netplotbrain examples. 
"""
#%% md
"""
Import all necessary packages
"""
#%%
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt

#%% md
"""
Load example data included in package.
"""
# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

#%%
# Plot single view
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view='SLR',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  nodecolorby='community')

plt.savefig('./examples/figures/singleview.png', dpi=150)

#%%
## Specify column names to specify size

fig = plt.figure()
ax_m1 = fig.add_subplot(121, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  fig = fig,
                  ax = ax_m1,
                  view='A',
                  nodes=nodes,
                  title='Centrality Measure 1',
                  nodesize='centrality_measure1',
                  nodecolor='red',
                  edges=edges)

ax_m2 = fig.add_subplot(122, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  fig = fig,
                  ax = ax_m2,
                  view='A',
                  nodes=nodes,
                  title='Centrality Measure 2',
                  nodesize='centrality_measure2',
                  nodecolor='blue',
                  edges=edges)
                  
plt.savefig('./examples/figures/measures.png', dpi=150)

#%%
## Plot multiple rows

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  nodecolorby='community',
                  view=['LSR', 'AIP'],
                  frames=2)
                  
plt.savefig('./examples/figures/rows1.png', dpi=150)

#%%
## Plot atlas (as nodes) from templateflow

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                            'desc': '400Parcels7Networks',
                            'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  title='Plotting templateflow atlas as spheres',
                  templatestyle='surface',
                  view=['LSR'],
                  nodetype='circles')
                  
plt.savefig('./examples/figures/atlas_circles.png', dpi=150)

#%%
## plot atlas (as parcels) from templateflow

netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                            'desc': '400Parcels7Networks',
                            'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  title='Plotting templateflow atlas as parcels',
                  templatestyle=None,
                  view=['LSR'],
                  nodetype='parcels',
                  nodealpha=0.5,
                  nodecolor='Set3')
                  
plt.savefig('./examples/figures/atlas_parcels.png', dpi=150)

#%%
## Plot individual hemispheres

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['SSS'],
                  hemisphere=['L', 'R', ''],
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges)
                  
plt.savefig('./examples/figures/hemi.png', dpi=150)

## Plot different templates

# Setting templatevoxsize to 0.2 will make it slightly quicker
# Due to the voxel size being smaller, the nodes are currently smaller
# So scaling the nodes is useful.  
netplotbrain.plot(template='WHS',
         templatestyle='surface',
         title='Multiple templates possible',
         view='LSR',
         nodes=nodes / 8,
         nodesize='centrality_measure1',
         edges=edges,
         nodecolorby='community',
         nodescale=80,
         templatevoxsize=0.2)

plt.savefig('./examples/figures/template_whs.png', dpi=150)

#%%
## Plot different styles

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='filled',
                  view='SPR',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges)
                  
plt.savefig('./examples/figures/styles1.png', dpi=150)




netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='cloudy',
                  view='SPR',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  templatevoxsize=2)
                  
plt.savefig('./examples/figures/styles2.png', dpi=150)
