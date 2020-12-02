
def _plot_nodes(ax, nodes, nodesize=50, nodecolor='salmon'):
    """
    Function that plots nodes in figure

    Parameters
    ---------------
    ax : matplotlib ax
    nodes : dataframe
        node dataframe with x, y, z coordinates. 
    nodesize : string or float, int
        if string, must refer to a column in nodes.
    nodecolor : string or matplotlib color
        if non-color string, must refer to a column in nodes

    Returns
    -------------
    Nothing 

    """
    # Check if nodesize input is column in node data
    if isinstance(nodesize, str) and nodesize in nodes.columns:
        ns = nodes[nodesize]
    else:
        ns = nodesize
    # Set colormap
    nc = nodecolor
    ax.scatter(nodes['x'], nodes['y'], nodes['z'], s=ns, color=nc)

def _scale_nodes(nodes, affine=None):
    """
    Scales nodes from MNI coordinates to ax with origin of 0.
    
    Parameters
    ---------------
    nodes : dataframe
        node dataframe with x, y, z coordinates. 
    affine : array
        3x4 array from img.affine (nibabel image). 

    Returns
    ----------------
    nodes : dataframe
        node dataframe with recaled x, y, z coordinates to account for affine matrix. 

    """
    nodes_scaled = nodes.copy()
    if affine is not None:
        nodes_scaled['x'] = (nodes_scaled['x'] - affine[0, -1]) / affine[0, 0]
        nodes_scaled['y'] = (nodes_scaled['y'] - affine[1, -1]) / affine[1, 1]
        nodes_scaled['z'] = (nodes_scaled['z'] - affine[2, -1]) / affine[2, 2]
    return nodes_scaled
