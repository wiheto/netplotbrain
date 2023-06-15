import numpy as np
from matplotlib import transforms
import pandas as pd

def _plot_connectivitymatrix(ax, edges, nodes=None, node_color=None, node_colorby=None, **kwargs):
    """Plot connectivity matrix

    Args:
        ax (matplotlib ax)
        edges (pandas datafram): edges.
    """

    # Dataframe to array
    if isinstance(nodes, pd.DataFrame):
        number_of_nodes=len(nodes)+1
    else:
        number_of_nodes=edges[['i', 'j']].max().max()+1

    cm_order = kwargs.get('cm_order')
    cm_boundary = kwargs.get('cm_boundary')
    cm_boundarywidth = kwargs.get('cm_boundarywidth')
    cm_border = kwargs.get('cm_border')
    cm_borderwidth = kwargs.get('cm_borderwidth')
    cm_bordercolor = kwargs.get('cm_bordercolor')
    vmin = kwargs.get('cm_vmin')
    vmax = kwargs.get('cm_vmax')
    #if cm_boundary == 'Auto' and (cm)
    #if cm_boundarycolor == 'auto' and cm_boundary is not None:
    #    cm_boundarycolor = 'black'
    #else:
    #    cm_boundarycolor = None
    if cm_order is not None:
        if cm_order == 'auto' and node_colorby is not None:
            cm_order = node_colorby
            if cm_boundary == 'auto': 
                cm_boundary = True
        communities = nodes[cm_order].astype('category').cat.codes.values
        nodeorder = np.argsort(communities)
    # If it is still set to auto, set ot None
    if cm_boundary == 'auto':
        cm_boundary = None

    adj = np.zeros((number_of_nodes, number_of_nodes))
    if 'weight' in edges:
        adj[edges['i'], edges['j']] = edges['weight']
        # TODO Assume the matrix is symmetric, fix later in kwargs
        adj[edges['j'], edges['i']] = edges['weight']
    else:
        adj[edges['i'], edges['j']] = 1
        # TODO Assume the matrix is symmetric, fix later in kwargs
        adj[edges['j'], edges['i']] = 1

    # rotate the plot
    rotate = kwargs.get('cm_rotate')
    if rotate:
        tr = transforms.Affine2D().rotate_deg(45) + ax.transData
    else:
        tr = ax.transData
    ax.pcolormesh(adj[nodeorder][:, nodeorder], cmap='RdBu_r', vmin=vmin, vmax=vmax, transform=tr, rasterized=True, zorder=1)

    # Plot
    # Add squares for different communities to the connectivity plot
    if cm_boundary:
        for coms in np.unique(communities):
            no = np.where(communities[nodeorder] == coms)[0]
            ax.plot([no[0], no[0]], [no[0], no[-1]+1], color=node_color[nodeorder[no[0]]], linewidth=cm_boundarywidth, transform=tr,zorder=10)
            ax.plot([no[-1]+1, no[0]], [no[-1]+1, no[-1]+1], color=node_color[nodeorder[no[0]]], linewidth=cm_boundarywidth, transform=tr,zorder=10)
            ax.plot([no[0], no[-1]+1], [no[0], no[0]], color=node_color[nodeorder[no[0]]], linewidth=cm_boundarywidth, transform=tr,zorder=10)
            ax.plot([no[-1]+1, no[-1]+1], [no[0], no[-1]+1], color=node_color[nodeorder[no[0]]], linewidth=cm_boundarywidth, transform=tr,zorder=10)
    if cm_border:            
        ax.plot([0, 0], [0, len(nodes)], color=cm_bordercolor, linewidth=cm_borderwidth, transform=tr,zorder=5)
        ax.plot([len(nodes), 0], [len(nodes), len(nodes)], color=cm_bordercolor, linewidth=cm_borderwidth, transform=tr,zorder=5)
        ax.plot([0, len(nodes)], [0, 0], color=cm_bordercolor, linewidth=cm_borderwidth, transform=tr,zorder=5)
        ax.plot([len(nodes), len(nodes)], [0, len(nodes)], color=cm_bordercolor, linewidth=cm_borderwidth, transform=tr,zorder=150)
