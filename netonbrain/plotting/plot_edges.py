import numpy as np

def _plot_edges(ax, nodes, edges, edgewidth='auto', edgewidthscale=1, edgecolor='k'):
    """
    Plots the edges on the plot

    Parameters 
    ----------------------------
    ax : matplotlib ax
    nodes : dataframe
        node dataframe with x, y, z coordinates (at least). 
    edges : array or dataframe
        numpy array (adj matrix) or edgelist (df.columns = ['i', 'j', 'weight']) 
    edgewidth : 'auto', float, int
        Width of edges. If auto, uses weights from array or dataframes. 
    edgewidthscale : float, int
        For display purposes, scale edges by value. 
    edgecolor : matplotlib color
        Colour of edges

    Returns
    ----------------------
    Nothing
    """
    # If numpy array.
    # for e in list(zip(*np.where(edges!=0))):
    #     print(e)
    #     if edgewidth != 'auto':
    #         ew = edgewidth * edgewidthscale
    #     else:
    #         ew = edges[e] * edgewidthscale
    #     print(nodes.loc[list(e)]['x'])
    #     # NOTE CURRENTLY LOC IS FILTERING EDGES. CHECK FOR COMPATIBILITY WITH HOW NODES works elsewhere
    #     ax.plot(nodes.loc[list(e)]['x'], nodes.loc[list(e)]['y'], nodes.loc[list(e)]['z'], color=edgecolor, linewidth=ew)
    #if dataframe
    for e, row in edges.iterrows():
        if row['i'] != 0 and row['j'] != 0:
            if edgewidth != 'auto':
                ew = edgewidth * edgewidthscale
            else:
                ew = row['weight'] * edgewidthscale
            #print(nodes.loc[edges.values.tolist()]['x'])
            ax.plot(nodes.loc[list((row['i'],row['j']))]['x'], nodes.loc[list((row['i'],row['j']))]['y'], nodes.loc[list((row['i'],row['j']))]['z'], color=edgecolor, linewidth=ew)