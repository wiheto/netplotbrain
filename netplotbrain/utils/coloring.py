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


def _highlight_nodes(nodes, nodecolor, highlightnodes, **kwargs):
    """

    Returns
    -------
    nodecolor : array
        a N x 4 color array for colouring of nodes where alpha is set here.
    highlight_idx : array
        Binary array of N index indicating which nodes are highlighted (for edge purposes)
    """
    highlightlevel = kwargs.get('highlightlevel')
    nodealpha = kwargs.get('nodealpha')
    if isinstance(highlightnodes, dict):
        highlight_idx = nodes[highlightnodes.keys()] == highlightnodes.values()
        highlight_idx = np.squeeze(highlight_idx.values)
    elif isinstance(highlightnodes, str):
        if highlightnodes not in nodes:
            raise ValueError('If highlightnodes is a str it must be a column in nodes')
        highlightnodes = nodes[highlightnodes].values()
    else:
        highlight_idx = np.zeros(len(nodes))
        highlight_idx[highlightnodes] = 1
    if isinstance(nodecolor, str):
        nodecolor = _colorarray_from_string(nodecolor, len(nodes))
    if nodecolor.shape[1] == 3:
        nodecolor = np.hstack(
            [nodecolor, np.vstack([nodealpha]*len(nodecolor))])
    # dim the non-highlighted nodes
    nodecolor[highlight_idx == 0, 3] = nodealpha * (1 - highlightlevel)
    # Nodealpha is now set in nodecolor, so set as None to avoid any later problems
    nodealpha = None
    return nodecolor, highlight_idx, nodealpha



def _highlight_edges(edges, edgecolor, highlightedges, **kwargs):
    """
    """
    highlightlevel = kwargs.get('highlightlevel')
    edgealpha = kwargs.get('edgealpha')
    if isinstance(highlightedges, dict):
        highlight_idx = edges[highlightedges.keys()] == highlightedges.values()
        highlight_idx = np.squeeze(highlight_idx.values)
    elif isinstance(highlightedges, str):
        if highlightedges not in edges:
            raise ValueError('If highlightnodes is a str it must be a column in nodes')
        highlight_idx = np.zeros(len(edges))
        highlight_idx[edges[highlightedges] != 0] = 1
    else:
        highlight_idx = np.zeros(len(edges))
        highlight_idx[highlightedges] = 1
    if isinstance(edgecolor, str):
        edgecolor = _colorarray_from_string(edgecolor, len(edges))
    if edgecolor.shape[1] == 3:
        edgecolor = np.hstack(
            [edgecolor, np.vstack([edgealpha]*len(edgecolor))])
    # dim the non-highlighted edges
    edgecolor[highlight_idx == 0, 3] = edgealpha * (1 - highlightlevel)
    # Nodealpha is now set in nodecolor, so set as None to avoid any later problems
    edgealpha = None
    return edgecolor, highlight_idx, edgealpha


def assign_color(row, colordict):
    if pd.isnull(row):
        return np.array([1, 1, 1, 0])
    else:
        return colordict[row]


def _detect_coloring_type(nodes, nodecolorby, prespecified=None):
    """
    Follows a heuristic to detect if a colorby column is continuous or discrete.
    If there are more than 8 unique values, then the value is seen as continuous.
    Prespecified allows you to override the behaviour.
    """
    if prespecified is None or prespecified == 'auto':
        if nodes[nodecolorby].nunique(dropna=True) > 8:
            colorpropertytype = 'continuious'
        elif nodes[nodecolorby].nunique(dropna=True) <= 8:
            colorpropertytype = 'discrete'
    else:
        colorpropertytype = prespecified

    return colorpropertytype


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
    cmap = kwargs.get(datatype + 'cmap')
    color_vminvmax = kwargs.get(datatype + 'colorvminvmax')
    colortype = _detect_coloring_type(df, colorby)
    cmap = cm.get_cmap(cmap)
    if colortype == 'discrete':
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
        # This will occur if nodecolorvminvmax is not
        raise ValueError('Cannot determine color type')
    return color_array