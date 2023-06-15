#
# # Visualizing a single network
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/plot_connectivitymatrix.ipynb)
#
# ## Goal
# Here we are plot the nodes on the brain from the Schaefer atlas and plot the connectivity matrix next to it
#
# So this code may seem long but most of it is creating the data. 
#

# +
# Import packages
import templateflow.api as tf
import netplotbrain
import pandas as pd
import numpy as np
import itertools

#  
# STEP 1 - CREATE DATA
#

# # +
# Get template information
template = 'MNI152NLin2009cAsym'
atlas = 'Schaefer2018'
atlas_desc = '100Parcels7Networks'

# +
# Get and load the tsv file (information about the atlas)
atlas_path = tf.get(atlas=atlas,
                    template=template,
                    desc=atlas_desc,
                    extension='.tsv')
atlas_df = pd.read_csv(atlas_path, sep='\t')
atlas_df.head()

#+
# Create a column called "network" by extracting the relevant information from the column "name"
atlas_df['network'] = list(map(lambda x: x.split('_')[2], atlas_df.name.values))
atlas_df.head()

#+
# We need to create edges for this network. Let's make a 100x100 network where within network connections are 1, everything else is 0.
edges = np.zeros([100, 100])
for network in atlas_df['network'].unique():
    idx =  atlas_df[atlas_df['network']==network].index
    idx_pairs = np.array(list(itertools.combinations(idx, 2)))
    edges[idx_pairs[:, 0], idx_pairs[:, 1]] = 1
    edges[idx_pairs[:, 1], idx_pairs[:, 0]] = 1

#  
# STEP 2 - PLOT DATA
#

# +
# Nodes in connectivity will automatically be organized by node_color, unless cm_order is specified.
# We set edge_alpha to 0 so they are not visible in the brain images
# If nodecolor is specified the borders of the connectivity matrix will be drawn grouping and circling them in. 
netplotbrain.plot(nodes={'template': 'MNI152NLin2009cAsym',
                         'atlas': atlas,
                         'desc': atlas_desc,
                         'resolution': 1},
                  edges=edges,
                  edge_alpha = 0,
                  view='Sc',
                  node_type='parcels',
                  nodes_df=atlas_df,
                  title=None,
                  node_color='network',
                  node_cmap='Set2')
