import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from matplotlib import cm
import mplcursors

def _get_color(nodes, colorby='communities', cmap='plasma'):
    
    cat = np.unique(nodes[colorby])
    cmap = cm.get_cmap(cmap)
    colors = cmap(np.linspace(0, 1, len(cat)))
    colordict = dict(zip(cat, colors))
    nodes["Color"] = nodes[colorby].apply(lambda z:colordict[z])
        
def _plot_spheres(ax, nodes, nodecolor='salmon', colorby='communities', nodesize=20, nodescale=1, nodecols=['x', 'y', 'z'], alpha=None):
    """
    Function that plots spheres in figure

    Parameters
    ---------------
    ax : matplotlib ax
    nodes : dataframe
        node dataframe with x, y, z coordinates.
    nodesize : string or float, int
        if string, must refer to a column in nodes.
    nodescale : int
        factor to scale all nodes by
    nodecolor : string or matplotlib color
        if non-color string, must refer to a column in nodes
    nodecols : list of string
        name of node column coordinates in datadrame

    Returns
    -------------
    Nothing

    """
    
    # Loop through each node and plot a surface plot
    for index, row in nodes.iterrows():
        # Get the xyz coords for the node
        c = [row[nodecols[0]],
             row[nodecols[1]],
             row[nodecols[2]]]

        # Check if nodesize is in the dataframe
        if nodesize in nodes.keys():
            r = row[nodesize] * nodescale
        else:
            r = nodesize * nodescale

        u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]

        # Calculate the x,y,z coordinates of each sphere
        x = r*np.cos(u)*np.sin(v)
        y = r*np.sin(u)*np.sin(v)
        z = r*np.cos(v)
        
        if colorby is None:
            ax.plot_surface(c[0]+x, c[1]+y, c[2]+z,
                            color=nodecolor,
                            alpha=alpha)
        if colorby in nodes.keys():
            mplcursors.cursor((ax.plot_surface(c[0]+x, c[1]+y, c[2]+z,
                            color=_get_color(nodes),
                            alpha=alpha))
        
        