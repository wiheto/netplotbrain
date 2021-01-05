from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 


def _plot_spheres(ax, nodes, nodecolor='salmon'):
  
  for i, row in nodes.iterrows(): 
    #print(c, r)
    c = [row['x'], row['y'], row['z']]
    
    if "radius" in row.keys():
        r = row["radius"]
    else:
        r = 7
    
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    #print(u, v) 
    x = r*np.cos(u)*np.sin(v)
    #print(x)
    y = r*np.sin(u)*np.sin(v)
    z = r*np.cos(v)
    
    ax.plot_surface(c[0]+x, c[1]+y, c[2]+z, color=nodecolor, alpha=0.5*np.random.random()+0.5)
    #print(x-c[0])

if __name__=="__main__":
    
    nodex = np.array([42, -42, -40, 40, 12, -12, -18, 18])
    nodey = np.array([-60, -60, 40, 40, 56, 56, -44, -44])
    nodez = np.array([30, 30, -16, -16, 35, 35, 44, 44])
    
    nodes = pd.DataFrame(data={'x': nodex, 'y': nodey, 'z': nodez})
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    _plot_spheres(ax, nodes)

