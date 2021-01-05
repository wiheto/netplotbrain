from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

nodex = np.array([42, -42, -40, 40, 12, -12, -18, 18])
nodey = np.array([-60, -60, 40, 40, 56, 56, -44, -44])
nodez = np.array([30, 30, -16, -16, 35, 35, 44, 44])

list_radius = [10,3,7,4,7,9,3]

list_center=[(i,j,k) for i,j,k in zip(nodex,nodey,nodez)]

def plt_sphere(list_center, list_radius):
  for c, r in zip(list_center, list_radius): #c: 3-tuple of x,y,z coordinates, r: radius
    #print(c, r)
    ax = fig.gca(projection='3d')

    # draw sphere
    #voxel-based measurement of spherical objects, represented in a numpy array
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    #print(u, v)
    #multiply value 
    x = r*np.cos(u)*np.sin(v)
    #print(x)
    y = r*np.sin(u)*np.sin(v)
    z = r*np.cos(v)

    ax.plot_surface(x-c[0], y-c[1], z-c[2], color=np.random.choice(['g','b']), alpha=0.5*np.random.random()+0.5)
    #print(x-c[0])
    
fig = plt.figure()
plt_sphere(list_center, list_radius)