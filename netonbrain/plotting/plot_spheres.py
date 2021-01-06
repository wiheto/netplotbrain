import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 


def _plot_spheres(ax, nodes, nodecolor='salmon'):
    
  if 'centrality' in nodes.keys():
      ss = 'centrality'
    
      for i, row in nodes.iterrows(): 
        c = [row['x'], row['y'], row['z']]
        
        r = row[ss]/10
        
        u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
        
        x = r*np.cos(u)*np.sin(v)
        y = r*np.sin(u)*np.sin(v)
        z = r*np.cos(v)
        
        ax.plot_surface(c[0]+x, c[1]+y, c[2]+z, color=nodecolor, alpha=0.5*np.random.random()+0.5)
  else:
        r = 2      

if __name__=="__main__":
    
    nodex = np.array([42, -42, -40, 40, 12, -12, -18, 18])
    nodey = np.array([-60, -60, 40, 40, 56, 56, -44, -44])
    nodez = np.array([30, 30, -16, -16, 35, 35, 44, 44])
    
    # Some psuedo_centrality measure to demonstrate size
    centrality = np.array([30, 30, 50, 15, 20, 10, 5, 25])
    
    nodes = pd.DataFrame(data={'x': nodex, 'y': nodey, 'z': nodez, 'centrality': centrality})
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    _plot_spheres(ax, nodes)

    

