import networkx as nx
import pandas as pd
from ..plotting import _plot_nodes, _plot_edges

def _plot_springlayout(ax, nodes, edges, node_color, node_size, edge_color, edge_weights, highlight_nodes, **kwargs):
    """
    This funciton calculates and plots a spring layout for nodes/edges instead of on a brain.
    """
    # Get relevant kwargs
    edgecols = kwargs.get('edge_columnnames')
    seed = kwargs.get('seed')
    # nodecolumnname is not needed/problematic, so get rid of it from kwargs
    kwargs.pop('node_columnnames')
    # First convert to networkx
    network = nx.from_pandas_edgelist(edges, edgecols[0], edgecols[1], edge_weights)
    # Calculate spring board for each
    layout = nx.drawing.spring_layout(network, weight=edge_weights, seed=seed)
    # Insert layout into nodes
    layout_df = pd.DataFrame(layout).transpose()
    layout_df.columns = ['spring_x', 'spring_y']
    layout_df.sort_index(inplace=True)
    nodes = nodes.join(layout_df)
    # Add dummy z axis for plot
    nodes['spring_z'] = 0
    # Get edge plot properties (repeats plot_edges)
    sl_nodecols= ['spring_x', 'spring_y', 'spring_z']
    _plot_edges(ax, nodes, edges, edgewidth=edge_weights, edge_color=edge_color,
                highlight_nodes=highlight_nodes, node_columnnames=sl_nodecols, **kwargs)
    _plot_nodes(ax, nodes, node_columnnames=sl_nodecols,
               node_color=node_color, node_size=node_size, **kwargs)

