import matplotlib.cm as cm
import matplotlib.colors as pltcol
import numpy as np
import pandas as pd


def _colorarray_from_string(cmap, ncolors):
    """Get colormap array from string that loops through colors."""
    if cmap in pltcol.ColorConverter.colors.keys():
        colors = pltcol.to_rgba_array(pltcol.ColorConverter.colors[cmap])
        colors = np.vstack([colors] * ncolors)
    elif cmap[0] == '#':
        colors = pltcol.to_rgba_array(cmap)
        colors = np.vstack([colors] * ncolors)
    else:
        colors = cm.get_cmap(cmap).colors
        colors = colors * int(np.ceil(ncolors / len(colors)))
        colors = np.array(colors)
    return colors[:ncolors]


def _highlight_nodes(nodes, node_color, highlight_nodes, **kwargs):
    """

    Returns
    -------
    node_color : array
        a N x 4 color array for colouring of nodes where alpha is set here.
    highlight_idx : array
        Binary array of N index indicating which nodes are highlighted (for edge purposes)
    """
    highlightlevel = kwargs.get('highlightlevel')
    node_alpha = kwargs.get('node_alpha')
    # Default is None, set to 1 if highlight_nodes is called
    if node_alpha is None:
        node_alpha = 1
    if isinstance(highlight_nodes, dict):
        highlight_idx = nodes[highlight_nodes.keys()] == highlight_nodes.values()
        highlight_idx = np.squeeze(highlight_idx.values)
    elif isinstance(highlight_nodes, str):
        highlight_idx = nodes[highlight_nodes].values
    else:
        highlight_idx = np.zeros(len(nodes))
        highlight_idx[highlight_nodes] = 1
    if isinstance(node_color, str):
        node_color = _colorarray_from_string(node_color, len(nodes))
    if node_color.shape[1] == 3:
        node_color = np.hstack(
            [node_color, np.vstack([node_alpha]*len(node_color))])
    # dim the non-highlighted nodes
    node_color[highlight_idx == 0, 3] = node_alpha * (1 - highlightlevel)
    # node_alpha is now set in node_color, so set as None to avoid any later problems
    node_alpha = None
    return node_color, highlight_idx, node_alpha



def _highlight_edges(edges, edge_color, highlight_edges, **kwargs):
    """
    """
    highlightlevel = kwargs.get('highlightlevel')
    edge_alpha = kwargs.get('edge_alpha')
    # Default is None, set to 1 if highlighting is called
    if edge_alpha is None:
        edge_alpha = 1
    if isinstance(highlight_edges, dict):
        highlight_idx = edges[highlight_edges.keys()] == highlight_edges.values()
        highlight_idx = np.squeeze(highlight_idx.values)
    elif isinstance(highlight_edges, str):
        highlight_idx = np.zeros(len(edges))
        highlight_idx[edges[highlight_edges] != 0] = 1
    else:
        highlight_idx = np.zeros(len(edges))
        highlight_idx[highlight_edges] = 1
    if isinstance(edge_color, str):
        edge_color = _colorarray_from_string(edge_color, len(edges))
    if edge_color.shape[1] == 3:
        edge_color = np.hstack(
            [edge_color, np.vstack([edge_alpha]*len(edge_color))])
    # dim the non-highlighted edges
    edge_color[highlight_idx == 0, 3] = edge_alpha * (1 - highlightlevel)
    # node_alpha is now set in node_color, so set as None to avoid any later problems
    edge_alpha = None
    return edge_color, highlight_idx, edge_alpha


def assign_color(row, colordict):
    if pd.isnull(row):
        return np.array([1, 1, 1, 0])
    else:
        return colordict[row]


def _detect_coloring_type(nodes, node_colorby, prespecified=None):
    """
    Follows a heuristic to detect if a colorby column is continuous or discrete.
    If there are more than 8 unique values, then the value is seen as continuous.
    Prespecified allows you to override the behaviour.
    """
    if prespecified is None or prespecified == 'auto':
        # Get unique colors
        ucols = nodes[node_colorby].unique()
        ncols = nodes[node_colorby].nunique(dropna=True)
        cols_are_colorlike = list(map(lambda x: cm.colors.is_color_like(x), ucols))
        if sum(cols_are_colorlike) == ncols:
            colorpropertytype = 'column'
        elif ncols > 8:
            colorpropertytype = 'continuious'
        elif ncols <= 8:
            colorpropertytype = 'discrete'
    else:
        colorpropertytype = prespecified

    return colorpropertytype

def _get_cmap(cmap):
    """Returns either matplotlib cmap or creates a cmap from str

    Args : str or list
        maplotlib cmap (string) or list of matplotlib colors

    Returns : cmap
        maptlotlib cmap
    """
    if isinstance(cmap, str):
        cmap = cm.get_cmap(cmap)
    elif isinstance(cmap, list):
        cmap = pltcol.ListedColormap(cmap)
    return cmap

def _get_colorby_colors(df, colorby, datatype='node', **kwargs):
    """
    Get array of different colors by some column

    Parameters
    -------------------
    df : dataframe
        dataframe to look in for colorby argument (nodes or edges dataframe)
    colorby : str
        column in dataframe
    datatype : str
        node or edge

    Returns
    -------------------
    color_array : numpy array
        A N x 4 list of matplotlib colours for each node
    """
    # Get relevant kwargs
    cmap = kwargs.get(datatype + '_' + 'cmap')
    color_vminvmax = kwargs.get(datatype + '_colorvminvmax')
    #TODO: Add flag if colours are in column
    colortype = _detect_coloring_type(df, colorby)

    cmap = _get_cmap(cmap)
    if colortype == 'column':
        color_array = cm.colors.to_rgba_array(df[colorby])
    elif colortype == 'discrete':
        cat = np.unique(df[colorby].dropna())
        colors = cmap(np.linspace(0, 1, len(cat)))
        colordict = dict(zip(cat, colors))
        color_array = df[colorby].apply(lambda z: assign_color(z, colordict))
        color_array = np.vstack(color_array.values)
    elif color_vminvmax == 'minmax':
        cat = df[colorby]
        cat = (cat - np.nanmin(cat)) / (np.nanmax(cat) - np.nanmin(cat))
        color_array = cmap(cat)
    elif color_vminvmax == 'maxabs':
        cat = df[colorby]
        cat = (cat - -np.nanmax(np.abs(cat))) / (np.nanmax(np.abs(cat)) - -np.nanmax(np.abs(cat)))
        color_array = cmap(cat)
    elif isinstance(color_vminvmax, list):
        cat = df[colorby]
        cat = (cat - -np.nanmax(np.abs(cat))) / (np.nanmax(np.abs(cat)) - -np.nanmax(np.abs(cat)))
        color_array = cmap(cat)
    else:
        # This will occur if node_colorvminvmax is not
        raise ValueError('Cannot determine color type')
    return color_array