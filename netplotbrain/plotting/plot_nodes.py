import numpy as np
from ..utils import _node_scale_vminvmax

def _plot_nodes(ax, nodes, nodecolumnnames, nodecolor='salmon', nodesize=20, **kwargs):
    """
    Function that plots nodes in figure

    Parameters
    ---------------
    ax : matplotlib ax
    nodes : dataframe
        node dataframe with x, y, z coordinates, must include nodecolumnnames.
    nodecolumnnames : list of string
        name of node column coordinates in datadrame.
    nodesize : string or float, int
        if string, must refer to a column in nodes.
    nodecolor : string or matplotlib color
        if non-color string, must refer to a column in nodes
    nodescale : float
        Scaling factor applied to nodesize.


    Returns
    -------------
    Nothing

    """
    # Get relevant kwargs
    nodescale = kwargs.get('nodescale')
    nodealpha = kwargs.get('nodealpha')
    # If half hemisphere is plotted, then cut the right
    nc = nodecolor
    if isinstance(nodecolor, np.ndarray):
        if len(nodes) < nodecolor.shape[0]:
            nc = nodecolor[nodes.index, :]
    # Check if nodesize input is column in node data
    if isinstance(nodesize, str) and nodesize in nodes.columns:
        ns = _node_scale_vminvmax(nodes, nodesize, **kwargs)
    else:
        ns = nodesize * nodescale
    ax.scatter(nodes[nodecolumnnames[0]], nodes[nodecolumnnames[1]],
               nodes[nodecolumnnames[2]], s=ns, color=nc, alpha=nodealpha)


def _scale_nodes(nodes, nodecolumnnames, affine=None):
    """
    Scales nodes from MNI coordinates to ax with origin of 0.

    Parameters
    ---------------
    nodes : dataframe
        node dataframe with x, y, z coordinates.
    nodecolumnnames : list of strings
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
        nodes_scaled[nodecolumnnames[0]] = (
            nodes_scaled[nodecolumnnames[0]] - affine[0, -1]) / affine[0, 0]
        nodes_scaled[nodecolumnnames[1]] = (
            nodes_scaled[nodecolumnnames[1]] - affine[1, -1]) / affine[1, 1]
        nodes_scaled[nodecolumnnames[2]] = (
            nodes_scaled[nodecolumnnames[2]] - affine[2, -1]) / affine[2, 2]
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
