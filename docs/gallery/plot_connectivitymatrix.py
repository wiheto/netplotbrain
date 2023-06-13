#  
# # Visualizing a single network
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/plot_connectivitymatrix.ipynb)
#
# ## Goal
# Here we are plot the nodes on the brain from the Schaefer atlas and plot the connectivity matrix next to it
#

# +
# Import packages
import templateflow.api as tf
import netplotbrain
import pandas as pd

# +
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

# +
# Nodes in connectivity will automatically be organized by node_color, unless cm_order is specified. 
netplotbrain.plot(nodes={'atlas': atlas,
                         'desc': atlas_desc,
                         'resolution': 1},
                  view='LSc', 
                  node_type='parcels', 
                  nodes_df=atlas_df, 
                  node_color='network', 
                  node_cmap='Set2')