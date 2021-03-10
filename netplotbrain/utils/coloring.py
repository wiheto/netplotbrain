import matplotlib.cm as cm
import matplotlib.colors as pltcol
import numpy as np



def _colorarray_from_string(cmap, ncolors):
    """
    Get colormap array from string that loops through colors
    """
    if cmap in pltcol.cnames or cmap[0] == '#': 
        colors = pltcol.to_rgba_array(cmap)
        colors = np.vstack([colors] * ncolors)
    else:
        colors = cm.get_cmap(cmap).colors
        colors = colors * int(np.ceil(ncolors / len(colors)))
        colors = np.array(colors)
    return colors[:ncolors]


def _highlight_nodes(nodes, nodecolor, nodealpha, highlightnodes, highlightlevel=0.75):
    if isinstance(highlightnodes, dict):
        highlight_idx = nodes[highlightnodes.keys()] == highlightnodes.values()
        highlight_idx = np.squeeze(highlight_idx.values)
    else:
        highlight_idx = np.zeros(len(nodes))
        highlight_idx[highlightnodes] = 1
    if isinstance(nodecolor, str): 
        nodecolor = _colorarray_from_string(nodecolor, len(nodes))
    if nodecolor.shape[1] == 3:
        nodecolor = np.hstack([nodecolor, np.vstack([nodealpha]*len(nodecolor))])
    # dim the non-highlighted nodes
    nodecolor[highlight_idx==0, 3] = nodealpha * (1 - highlightlevel)
    return nodecolor, highlight_idx



def _get_colorby_colors(df, colorby=None, cmap='plasma'):
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
    cat = np.unique(df[colorby])
    cmap = cm.get_cmap(cmap)
    colors = cmap(np.linspace(0, 1, len(cat)))
    colordict = dict(zip(cat, colors))
    color_array = df[colorby].apply(lambda z:colordict[z])
    color_array = np.vstack(color_array.values)
    return color_array