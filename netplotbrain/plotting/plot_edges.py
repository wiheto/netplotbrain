import numpy as np
import pandas as pd


def _npedges2dfedges(edges, edge_threshold=0, edge_thresholddirection='absabove'):
    """
    A function which transforms numpy array edges into dataframe.

    This function is required for compatiblity with other functions.

    Parameters
    ---------------------
    edges : numpy array
        n x n array of edges
    edge_threshold : float
        only find edges over a certain threshold
    edgetype : str
        Can be below, above or absabove. Default is absabove.
        This argument says if keeping edges<edge_threshold, below(edge<threshold), or abs(edges) above
    """
    if edge_thresholddirection == 'above':
        ind = np.where(edges > edge_threshold)
    if edge_thresholddirection == 'below':
        ind = np.where(edges < edge_threshold)
    if edge_thresholddirection == 'absabove':
        ind = np.where(np.abs(edges) > edge_threshold)
    weights = edges[ind]
    # Create dataframe
    df = pd.DataFrame(data={'i': ind[0], 'j': ind[1], 'weight': weights})
    return df


def _get_edge_highlight_alpha(node_i, node_j, highlight_nodes, **kwargs):
    edge_alpha = kwargs.get('edge_alpha')
    highlightlevel = kwargs.get('highlightlevel')
    edge_highlightbehaviour = kwargs.get('edge_highlightbehaviour')
    if len(highlight_nodes) == 0:
        highlight_nodes = None
    if edge_alpha is None:
        pass
    elif highlight_nodes is None or edge_highlightbehaviour is None:
        pass
    elif node_i in highlight_nodes and node_j in highlight_nodes and edge_highlightbehaviour == 'both':
        pass
    elif (node_i in highlight_nodes or node_j in highlight_nodes) and edge_highlightbehaviour == 'any':
        pass
    else:
        edge_alpha = edge_alpha * (1 - highlightlevel)
    return edge_alpha


def _plot_edges(ax, nodes, edges, edgewidth=None, edge_color='k', highlight_nodes=None, **kwargs):
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
    edge_widthscale : float, int
        For display purposes, scale edges by value.
    edge_color : matplotlib color
        Colour of edges
    edgecol : list (2 elements). Default: ['i', 'j']
        list of length 2.
        The first two, reference the node indicies in nodes.
        The third referencees the weights.
    highlight_nodes : list
        See netplotbrain.plot
    highlightlevel : float
        See netplotbrain.plot
    edge_highlightbehaviour : str
        alternatives "both" or "any" or None.
        Governs edge dimming when highlight_nodes is on
        If both, then highlights only edges between highlighted nodes.
        If any, then only edges connecting any of the nodes are highlighted.

    kwargs
    ---------------------
    edge_alpha : float
        Transparency of edges.

    Returns
    ----------------------
    Nothing
    """
    edgecol = kwargs.get('edge_columnnames')
    nodecol = kwargs.get('node_columnnames')
    edge_widthscale = kwargs.get('edge_widthscale')
    # Convert highlight_nodes binary list to index list
    hl_idx = np.where(np.array(highlight_nodes) == 1)[0]
    # if set as a string
    ec = edge_color
    # Because while edge_color (when array) and edges can be same size, if edge_threshold is set, indicies can be off due to merge
    # So eci is a separate counter instead of using the auto index in iterrows (which takes df index).
    eci = 0
    for _, row in edges.iterrows():
        # if row[edgecol[0]] != 0 and row[edgecol[1]] != 0:
        if isinstance(edge_color, np.ndarray):
            if edge_color.shape[0] == len(edges):
                ec = edge_color[eci, :]
        if edgewidth is None:
            ew = edge_widthscale
        else:
            ew = row[edgewidth] * edge_widthscale

        if row[edgecol[0]] in nodes.index and row[edgecol[1]] in nodes.index:
            ea = _get_edge_highlight_alpha(
                row[edgecol[0]], row[edgecol[1]], hl_idx, **kwargs)
            xp = nodes.loc[list((row[edgecol[0]], row[edgecol[1]]))][nodecol[0]]
            yp = nodes.loc[list((row[edgecol[0]], row[edgecol[1]]))][nodecol[1]]
            zp = nodes.loc[list((row[edgecol[0]], row[edgecol[1]]))][nodecol[2]]
            ax.plot(xp, yp, zp, color=ec, linewidth=ew, alpha=ea)
        eci += 1