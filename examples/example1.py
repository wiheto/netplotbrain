#%% md
"""
## The basics.
# This notebook goes through a showcase of netplotbrain examples.
"""
#%% 
# Import everything needed
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
                  template_style='surface',
                  view='LSR',
                  nodes=nodes,
                  node_scale=40,
                  node_size='centrality_measure1',
                  edges=edges,
                  node_color='community')

plt.savefig('./examples/figures/singleview.png', dpi=150)
plt.close('all')

#%%
## Specify column names to specify size

fig = plt.figure()
ax_m1 = fig.add_subplot(121, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='surface',
                  fig = fig,
                  ax = ax_m1,
                  view='A',
                  nodes=nodes,
                  title='Centrality Measure 1',
                  node_size='centrality_measure1',
                  node_color='red',
                  edges=edges,
                  showlegend=False)

ax_m2 = fig.add_subplot(122, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='surface',
                  fig = fig,
                  ax = ax_m2,
                  view='A',
                  nodes=nodes,
                  title='Centrality Measure 2',
                  node_size='centrality_measure2',
                  node_color='blue',
                  edges=edges,
                  showlegend=False)

fig.savefig('./examples/figures/measures.png', dpi=150)
plt.close('all')

#%%
## Plot multiple rows

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='surface',
                  nodes=nodes,
                  node_size='centrality_measure1',
                  edges=edges,
                  node_color='community',
                  view=['LSR', 'AIP'],
                  frames=2)

plt.savefig('./examples/figures/rows1.png', dpi=150)
plt.close('all')

#%%
## Plot atlas (as nodes) from templateflow

netplotbrain.plot(nodes={'atlas': 'Schaefer2018',
                            'desc': '400Parcels7Networks',
                            'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  title='Plotting templateflow atlas as spheres',
                  template_style='surface',
                  view=['LSR'],
                  node_type='circles')

plt.savefig('./examples/figures/atlas_circles.png', dpi=150)
plt.close('all')

#%%
## plot atlas (as parcels) from templateflow

netplotbrain.plot(nodes={'atlas': 'Schaefer2018',
                            'desc': '400Parcels7Networks',
                            'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  title='Plotting templateflow atlas as parcels',
                  template_style=None,
                  view=['LSR'],
                  node_type='parcels',
                  node_alpha=0.5,
                  node_color='Set3')

plt.savefig('./examples/figures/atlas_parcels.png', dpi=150)
plt.close('all')

#%%
## Plot individual hemispheres

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='surface',
                  view=['SSS'],
                  hemisphere=['L', 'R', ''],
                  nodes=nodes,
                  node_size='centrality_measure1',
                  edges=edges)

plt.savefig('./examples/figures/hemi.png', dpi=150)
plt.close('all')

## Plot different templates

# rat template
# Setting template_voxelsize to 0.2 will make it slightly quicker
# Due to the voxel size being smaller, the nodes are currently smaller
# So scaling the nodes is useful.
nodes_whs = nodes.copy()
nodes_whs['x'] = nodes_whs['x'] / 8
nodes_whs['y'] = nodes_whs['y'] / 8
nodes_whs['z'] = nodes_whs['z'] / 8
netplotbrain.plot(template='WHS',
         template_style='surface',
         title='Multiple templates possible',
         view='LSR',
         nodes=nodes_whs,
         node_size='centrality_measure1',
         edges=edges,
         node_color='community',
         node_scale=80,
         template_voxelsize=0.2)

plt.savefig('./examples/figures/template_whs.png', dpi=150)
plt.close('all')

#infant template
nodes_inf = nodes.copy()
nodes_inf['x'] = nodes_inf['x'] / 1.25
nodes_inf['y'] = nodes_inf['y'] / 1.25
nodes_inf['z'] = nodes_inf['z'] / 1.25
netplotbrain.plot(template='MNIInfant',
         template_style='surface',
         title='Infant template',
         view='LSR',
         nodes=nodes_inf,
         node_size='centrality_measure1',
         node_color='community',
         node_scale=80,
         edges=edges,
         template_voxelsize=5)

plt.savefig('./examples/figures/template_inf.png', dpi=150)
plt.close('all')

#%%
## Plot different styles

netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='filled',
                  view='SPR',
                  nodes=nodes,
                  node_size='centrality_measure1',
                  edges=edges,
                  template_voxelsize=5)

plt.savefig('./examples/figures/styles1.png', dpi=150)
plt.close('all')




netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='cloudy',
                  view='SPR',
                  nodes=nodes,
                  node_size='centrality_measure1',
                  edges=edges,
                  template_voxelsize=2)

plt.savefig('./examples/figures/styles2.png', dpi=150)
plt.close('all')
