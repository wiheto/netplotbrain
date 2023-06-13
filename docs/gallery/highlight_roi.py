#  
# # Highlight Parcels
#
# One possble use of netplotbrain is to highlight a seed region used. Here we will highlight two regions of interest. 

# +
# Load imports
import netplotbrain
import pandas as pd
import numpy as np

# Get 100 node atlas from templateflow
node_dict = {'atlas':       'Schaefer2018', 
             'desc':        '100Parcels7Networks',
             'extension':   '.nii.gz',
             'resolution':  1}

# pyton index of atlas rois. 
# this will start at 0 but atlas starts at 1.
# So below select node 15 and 66 in atlas. 
seeds = [14, 65]

# Create dataframe of 100 rois
nodeinfo = np.zeros(100)
nodeinfo[seeds] = 1

node_color = ['gray'] * 100
node_color[seeds[0]] = 'cornflowerblue'
node_color[seeds[1]] = 'salmon'
nodes_df = pd.DataFrame({'seed': nodeinfo, 'color': node_color})


fig, _ = netplotbrain.plot(template = 'MNI152NLin2009cAsym',
                  nodes =     node_dict,
                  nodes_df =  nodes_df,
                  node_type = 'parcels',
                  view =      'preset-3',
                  node_color = 'color',
                  highlight_nodes = 'seed',
                  highlighlevel = 1,
                  node_alpha = 0.4,
                  save_name='/home/xthowi/scratch/sham.png',
                  figdpi=300)
