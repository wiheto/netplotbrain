import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import random


def _plot_spheres(ax, nodes):
  
  """
  Function that plots spheres in figure
    
  Parameters
  ---------------
  ax : matplotlib ax
  nodes : dataframe
      node dataframe with x, y, z coordinates. 
  nodecolor : string or matplotlib color
      if non-color string, must refer to a column in nodes
    
  Returns
  -------------
  Nothing 
    
  """    
  
  if 'centrality' in nodes.keys():
      ss = 'centrality'
    
      for i, row in nodes.iterrows(): 
        c = [row['x'], row['y'], row['z']]
        
        r = row[ss]/10
        
        u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
        
        x = r*np.cos(u)*np.sin(v)
        y = r*np.sin(u)*np.sin(v)
        z = r*np.cos(v)
        
        random.seed(row[ss])
        
        red = random.random()
        g = random.random()
        b = random.random()
        
        node_color = [red,g,b]
                   
        ax.plot_surface(c[0]+x, c[1]+y, c[2]+z, color=node_color, alpha=0.5*np.random.random()+0.5)
  else:
        r = 2      

    




