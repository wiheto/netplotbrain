import networkx as nx
import pandas as pd
import numpy as np
from ..plotting import _plot_nodes, _plot_edges

def _plot_springlayout(ax, nodes, edges, nodecolor, nodesize, edgecolor, edgeweights, highlightnodes, **kwargs):
    """
    This funciton calculates and plots a spring layout for nodes/edges instead of on a brain.
    """
    # Get relevant kwargs
    edgecols = kwargs.get('edgecolumnnames')
    seed = kwargs.get('seed')
    # nodecolumnname is not needed/problematic, so get rid of it from kwargs
    kwargs.pop('nodecolumnnames')
    # First convert to networkx
    network = nx.from_pandas_edgelist(edges, edgecols[0], edgecols[1], edgeweights)
    # Calculate spring board for each
    layout = nx.drawing.spring_layout(network, weight=edgeweights, seed=seed)
    # Insert layout into nodes
    layout_df = pd.DataFrame(layout).transpose()
    layout_df.columns = ['spring_x', 'spring_y']
    layout_df.sort_index(inplace=True)
    nodes = nodes.join(layout_df)
    # Add dummy z axis for plot
    nodes['spring_z'] = 0
    # Get edge plot properties (repeats plot_edges)
    sl_nodecols= ['spring_x', 'spring_y', 'spring_z']
    _plot_edges(ax, nodes, edges, edgewidth=edgeweights, edgecolor=edgecolor,
                highlightnodes=highlightnodes, nodecolumnnames=sl_nodecols, **kwargs)
    _plot_nodes(ax, nodes, nodecolumnnames=sl_nodecols,
               nodecolor=nodecolor, nodesize=nodesize, **kwargs)

