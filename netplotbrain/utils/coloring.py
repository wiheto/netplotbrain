import matplotlib.cm as cm
import matplotlib.colors as pltcol
import numpy as np
import pandas as pd


def _colorarray_from_string(cmap, ncolors):
    """Get colormap array from string that loops through colors."""
    if cmap in pltcol.cnames or cmap[0] == '#':
        colors = pltcol.to_rgba_array(cmap)
        colors = np.vstack([colors] * ncolors)
    else:
        colors = cm.get_cmap(cmap).colors
        colors = colors * int(np.ceil(ncolors / len(colors)))
        colors = np.array(colors)
    return colors[:ncolors]


def _highlight_nodes(nodes, nodecolor, highlightnodes, **kwargs):
    highlightlevel = kwargs.get('highlightlevel')
    nodealpha = kwargs.get('nodealpha')
    if isinstance(highlightnodes, dict):
        highlight_idx = nodes[highlightnodes.keys()] == highlightnodes.values()
        highlight_idx = np.squeeze(highlight_idx.values)
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
    return nodecolor, highlight_idx


def assign_color(row, colordict):
    if pd.isnull(row):
        return np.array([1, 1, 1, 0])
    else:
        return colordict[row]


def _detect_nodecolor_type(nodes, nodecolorby, prespecified=None):
    """
    Follows a heuristic to detect if a colorby column is continuous or discrete.
    If there are more than 8 unique values, then the value is seen as continuous.
    Prespecified allows you to override the behaviour.
    """
    if prespecified is None or prespecified == 'auto':
        if nodes[nodecolorby].nunique() > 8:
            colorpropertytype = 'continuious'
        elif nodes[nodecolorby].nunique() <= 8:
            colorpropertytype = 'discrete'
    else:
        colorpropertytype = prespecified

    return colorpropertytype


def _get_colorby_colors(df, colorby, cmap='plasma', **kwargs):
    """
    Get array of different colors by some column

    Parameters
    -------------------
    df : dataframe
        dataframe to look in for colorby argument (nodes or edges dataframe)
    colorby : str
        column in dataframe
    cmap : colormap

    Returns
    -------------------
    color_array : numpy array
        A N x 4 list of matplotlib colours for each node
    """
    node_color_vminvmax = kwargs.get('nodecolorvminvmax')
    nodecolortype = _detect_nodecolor_type(df, colorby)
    cmap = cm.get_cmap(cmap)
    if nodecolortype == 'discrete':
        cat = np.unique(df[colorby])
        colors = cmap(np.linspace(0, 1, len(cat)))
        colordict = dict(zip(cat, colors))
        color_array = df[colorby].apply(lambda z: assign_color(z, colordict))
        color_array = np.vstack(color_array.values)
    elif node_color_vminvmax == 'minmax':
        cat = df[colorby]
        cat = (cat - np.min(cat)) / (np.max(cat) - np.min(cat))
        color_array = cmap(cat)
    elif node_color_vminvmax == 'maxabs':
        cat = df[colorby]
        cat = (cat - -np.max(np.abs(cat))) / (np.max(np.abs(cat)) - -np.max(np.abs(cat)))
        color_array = cmap(cat)
    elif isinstance(node_color_vminvmax, list):
        cat = df[colorby]
        cat = (cat - -np.max(np.abs(cat))) / (np.max(np.abs(cat)) - -np.max(np.abs(cat)))
        color_array = cmap(cat)
    else:
        print(nodecolortype)
        print(node_color_vminvmax)
        # This will occur if nodecolorvminvmax is not
        raise ValueError('Cannot determine color type')
    return color_array