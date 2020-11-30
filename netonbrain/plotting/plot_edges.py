import numpy as np

def _plot_edges(ax, nodes, edges, edgewidth='auto', edgewidthscale=1, edgecolor='k'):
    """
    edges,
    """
    # If numpy array.
    for e in list(zip(*np.where(edges!=0))):
        if edgewidth != 'auto':
            ew = edgewidth * edgewidthscale
        else:
            ew = edges[e] * edgewidthscale
        # NOTE CURRENTLY LOC IS FILTERING EDGES. CHECK FOR COMPATIBILITY WITH HOW NODES works elsewhere
        ax.plot(nodes.loc[list(e)]['x'], nodes.loc[list(e)]['y'], nodes.loc[list(e)]['z'], color=edgecolor, linewidth=ew)
