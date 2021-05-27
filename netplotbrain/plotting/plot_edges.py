import numpy as np
import pandas as pd


def _npedges2dfedges(edges, edgethreshold=0):
    """
    A function which transforms numpy array edges into dataframe.

    This function is required for compatiblity with other functions.

    Parameters
    ---------------------
    edges : numpy array
        n x n array of edges
    edgethreshold : float
        only find edges over a certain threshold
    """
    ind = np.where(edges > edgethreshold)
    weights = edges[ind]
    # Create dataframe
    df = pd.DataFrame(data={'i': ind[0], 'j': ind[1], 'weight': weights})
    return df


def _get_edge_highlight_alpha(node_i, node_j, highlightnodes, **kwargs):
    edgealpha = kwargs.get('edgealpha')
    highlightlevel = kwargs.get('highlightlevel')
    edgehighlightbehaviour = kwargs.get('edgehighlightbehaviour')
    if highlightnodes is None or edgehighlightbehaviour is None:
        pass
    elif node_i in highlightnodes and node_j in highlightnodes and edgehighlightbehaviour == 'both':
        pass
    elif (node_i in highlightnodes or node_j in highlightnodes) and edgehighlightbehaviour == 'any':
        pass
    else:
        edgealpha = edgealpha * (1 - highlightlevel)
    return edgealpha


def _plot_edges(ax, nodes, edges, edgewidth=None, edgecolor='k', highlightnodes=None, **kwargs):
    """
    Plots the edges on the plot.

    Parameters
    ----------------------------
    ax : matplotlib ax
    nodes : dataframe
        node dataframe with x, y, z coordinates (at least).
    edges : array or dataframe
        numpy array (adj matrix) or edgelist (df.columns = ['i', 'j', ...])
    edgewidth : string
        Column pointing to edges.
    edgewidthscale : float, int
        For display purposes, scale edges by value.
    edgecolor : matplotlib color
        Colour of edges
    edgecol : list (2 elements). Default: ['i', 'j']
        list of length 2.
        The first two, reference the node indicies in nodes.
        The third referencees the weights.
    highlightnodes : list
        See netplotbrain.plot
    highlightlevel : float
        See netplotbrain.plot
    edgehighlightbehaviour : str
        alternatives "both" or "any" or None.
        Governs edge dimming when highlightnodes is on
        If both, then highlights only edges between highlighted nodes.
        If any, then only edges connecting any of the nodes are highlighted.

    kwargs
    ---------------------
    edgealpha : float
        Transparency of edges.

    Returns
    ----------------------
    Nothing
    """
    edgecol = kwargs.get('edgecolumnnames')
    edgewidthscale = kwargs.get('edgewidthscale')
    # Convert highlightnodes binary list to index list
    hl_idx = np.where(np.array(highlightnodes) == 1)[0]
    # if dataframe
    for _, row in edges.iterrows():
        # if row[edgecol[0]] != 0 and row[edgecol[1]] != 0:
        if edgewidth is None:
            ew = edgewidthscale
        else:
            ew = row[edgewidth] * edgewidthscale
        if row[edgecol[0]] in nodes.index and row[edgecol[1]] in nodes.index:
            ea = _get_edge_highlight_alpha(
                row[edgecol[0]], row[edgecol[1]], hl_idx, **kwargs)
            xp = nodes.loc[list((row[edgecol[0]], row[edgecol[1]]))]['x']
            yp = nodes.loc[list((row[edgecol[0]], row[edgecol[1]]))]['y']
            zp = nodes.loc[list((row[edgecol[0]], row[edgecol[1]]))]['z']
            ax.plot(xp, yp, zp, color=edgecolor, linewidth=ew, alpha=ea)
