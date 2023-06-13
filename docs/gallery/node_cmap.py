#  
# # Specifying node colormaps
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/node_cmap.ipynb)
#
# See [example about colors for different way the color columns in the dataframe can be specified](https://www.netplotbrain.org/gallery/specifying_node_color/) 
#
# There are two different ways to specify colormaps. This holds for both nodes (node_cmap) edges (edge_cmap)
#
# The first way entails that you specify a matplotlib colormap (e.g. Set1, Inferno, (see options [here](https://matplotlib.org/stable/tutorials/colors/colormaps.html)) 
#
# The second way is to provide a list of matplotlib colors to create your own colormap (see named color options [here](https://matplotlib.org/stable/gallery/color/named_colors.html))
#
# This notebook will shows an example of each of these. We will use 100 ROIs from the Schaefer atlas and color the 7 Yeo networks

# Import necessary packages 
import netplotbrain
import pandas as pd
import templateflow.api as tf

# Load templateflow information about the Schaefer atlas
atlasinfo = tf.get(template='MNI152NLin2009cAsym',
                   atlas='Schaefer2018',
                   desc='100Parcels7Networks',
                   extension='.tsv')
atlas_df = pd.read_csv(str(atlasinfo), sep='\t')
atlas_df.head()

# Create a column called "network" by extracting the relevant information from the column "name"
atlas_df['network'] = list(map(lambda x: x.split('_')[2], atlas_df.name.values))
atlas_df.head()

# Define the TemplateFlow parcels that we want to plot 
nodes = {'template': 'MNI152NLin2009cAsym',
         'atlas': 'Schaefer2018',
         'desc': '100Parcels7Networks',
         'resolution': 1}

# Plot with a the Set2 colormap
netplotbrain.plot(nodes=nodes, 
                  node_type='parcels', 
                  nodes_df=atlas_df, 
                  node_color='network', 
                  node_cmap='Set2')

# Create custom colormap
node_cmap = ['blue', 'red', 'green', 'black', 'purple', 'yellow', 'orange']

# Plot with a the custom colormap
netplotbrain.plot(nodes=nodes, 
                  node_type='parcels', 
                  nodes_df=atlas_df, 
                  node_color='network', 
                  node_cmap=node_cmap)
