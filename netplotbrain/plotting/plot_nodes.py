import numpy as np
from ..utils import _node_scale_vminvmax
from scipy.spatial.distance import euclidean

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

# Function to check if a point is occupied in the plot
def is_point_occupied(ax, point):
    result = ax.transData.transform([point[:2]])
    return ax.contains_point(result[0]) 

def find_empty_spot_around_node(center_coord, ax):
    max_tries = 100
    for _ in range(max_tries):
        random_offset = np.random.uniform(low=-50, high=50, size=3)
        candidate_coord = center_coord + random_offset
        if not is_point_occupied(ax, candidate_coord):
            return candidate_coord
    return None  # Return None if no unoccupied spot is found after max_tries

def _add_node_text(ax, nodes, node_text, node_colmnnames, node_text_style):
    """
    Prints node text around nodes in figure. 
    
    Parameters
    --------------
    nodes : dataframe
        node dataframe with x, y, z coordinates.
    node_text : string
        column name of node text in nodes.
    node_columnnames : list of strings
        column names of x, y, z coordinates
    node_text_style : string
        can be center or arrow which determines how the text is plotted.
    """
    
    if node_text_style == 'center':
        for i, row in nodes.iterrows():
            if not np.isnan(row[node_text]):
                ax.text(row[node_colmnnames[0]], row[node_colmnnames[1]],
                        row[node_colmnnames[2]], row[node_text], fontsize=8, ha='center', va='center')
    else:
        raise ValueError('node_text_style must be center or arrow')
    
    
    
def _add_node_text(ax, nodes, node_text, node_colmnnames, node_text_style):
    """
    Prints node text around nodes in figure. 
    
    Parameters
    --------------
    nodes : dataframe
        node dataframe with x, y, z coordinates.
    node_text : string
        column name of node text in nodes.
    node_columnnames : list of strings
        column names of x, y, z coordinates
    node_text_style : string
        can be center or arrow which determines how the text is plotted.
    """
    if node_text_style == 'center':
        for i, row in nodes.iterrows():
            if not np.isnan(row[node_text]):
                ax.text(row[node_colmnnames[0]], row[node_colmnnames[1]],
                        row[node_colmnnames[2]], row[node_text], fontsize=8, ha='center', va='center')
    elif node_text_style == 'arrow':
        for i, row in nodes.iterrows():
            if not np.isnan(row[node_text]):
                # Define a grid of candidate coordinates around center_coord
                grid_size = 10
                center_coord = row[node_colmnnames]
                x_grid, y_grid, z_grid = np.meshgrid(
                    np.linspace(center_coord[0] - 100, center_coord[0] + 100, grid_size),
                    np.linspace(center_coord[1] - 100, center_coord[1] + 100, grid_size),
                    np.linspace(center_coord[2] - 100, center_coord[2] + 100, grid_size),
                )
                # Flatten the grid to iterate over each point
                candidate_coords = list(zip(x_grid.flatten(), y_grid.flatten(), z_grid.flatten()))

                # Find the closest empty spot using scipy's euclidean function
                min_distance = float('inf')
                closest_empty_spot = None

                for coord in candidate_coords:
                    if not is_point_occupied(ax, coord):
                        distance = euclidean(center_coord, coord)
                        if distance < min_distance:
                            min_distance = distance
                            closest_empty_spot = coord                
                # Draw a line from center_coord to the empty_spot
                ax.plot([row[node_colmnnames[0]], closest_empty_spot[0]],
                        [row[node_colmnnames[1]], closest_empty_spot[1]],
                        [row[node_colmnnames[2]], closest_empty_spot[2]], color='gray')

                ax.text(*closest_empty_spot, row[node_text], fontsize=8, color='black', ha='center', va='center')
    else:
        raise ValueError('node_text_style must be center or arrow')
         
    
