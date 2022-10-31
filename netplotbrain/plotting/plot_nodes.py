import numpy as np
from ..utils import _node_scale_vminvmax

def _plot_nodes(ax, nodes, node_columnnames, node_color='salmon', node_size=20, **kwargs):
    """
    Function that plots nodes in figure

    Parameters
    ---------------
    ax : matplotlib ax
    nodes : dataframe
        node dataframe with x, y, z coordinates, must include node_columnnames.
    node_columnnames : list of string
        name of node column coordinates in datadrame.
    node_size : string or float, int
        if string, must refer to a column in nodes.
    node_color : string or matplotlib color
        if non-color string, must refer to a column in nodes
    node_scale : float
        Scaling factor applied to node_size.


    Returns
    -------------
    Nothing

    """
    # Get relevant kwargs
    node_scale = kwargs.get('node_scale')
    node_alpha = kwargs.get('node_alpha')
    # If half hemisphere is plotted, then cut the right
    nc = node_color
    if isinstance(node_color, np.ndarray):
        if len(nodes) < node_color.shape[0]:
            nc = node_color[nodes.index, :]
    # Check if node_size input is column in node data
    if isinstance(node_size, str) and node_size in nodes.columns:
        ns = _node_scale_vminvmax(nodes, node_size, **kwargs)
    else:
        ns = node_size * node_scale
    ax.scatter(nodes[node_columnnames[0]], nodes[node_columnnames[1]],
               nodes[node_columnnames[2]], s=ns, color=nc, alpha=node_alpha)


def _scale_nodes(nodes, node_columnnames, affine=None):
    """
    Scales nodes from MNI coordinates to ax with origin of 0.

    Parameters
    ---------------
    nodes : dataframe
        node dataframe with x, y, z coordinates.
    node_columnnames : list of strings
        column names of x, y, z coordinates
    affine : array
        3x4 array from img.affine (nibabel image).

    Returns
    ----------------
    nodes : dataframe
        node dataframe with recaled x, y, z coordinates to account for affine matrix.

    """
    nodes_scaled = nodes.copy()
    if affine is not None:
        nodes_scaled[node_columnnames[0]] = (
            nodes_scaled[node_columnnames[0]] - affine[0, -1]) / affine[0, 0]
        nodes_scaled[node_columnnames[1]] = (
            nodes_scaled[node_columnnames[1]] - affine[1, -1]) / affine[1, 1]
        nodes_scaled[node_columnnames[2]] = (
            nodes_scaled[node_columnnames[2]] - affine[2, -1]) / affine[2, 2]
    return nodes_scaled


def _select_single_hemisphere_nodes(nodes, nodecol, affine, hemisphere):
    """
    Only take nodes from datafrom that match requested hemisphere.

    The function assumes that it is the x column in the MRI data.

    Parameters
    -------------
    nodes : dataframe
    nodecol : str
        Single dimension of the hemisphere column.
    affine : array
    hesmiphere : str
    """
    if hemisphere == 'left' or hemisphere == 'L':
        sel = nodes[nodecol] * affine[0, 0] < np.abs(affine[0, -1])
        nodes = nodes[sel]
    elif hemisphere == 'right' or hemisphere == 'R':
        sel = nodes[nodecol] * affine[0, 0] > np.abs(affine[0, -1])
        nodes = nodes[sel]
    return nodes
