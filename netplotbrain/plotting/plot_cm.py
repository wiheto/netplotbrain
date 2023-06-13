import numpy as np
from matplotlib import transforms
import pandas as pd

def _plot_connectivitymatrix(ax, edges, nodes=None, node_colorby=None, **kwargs):
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
    if cm_order is not None:
        if cm_order == 'auto' and node_colorby is not None:
            cm_order = node_colorby
        nodeorder = np.argsort(nodes[cm_order].astype('category').cat.codes.values)


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
        tr = transforms.Affine2D().rotate_deg(45)
    # Plot
    ax.pcolormesh(adj[nodeorder][:, nodeorder], cmap='RdBu_r', vmin=-1, vmax=1, transform=tr + ax.transData, rasterized=True)
