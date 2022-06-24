import netplotbrain
import pytest
import pandas as pd
import numpy as np
import networkx as nx

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

g = nx.Graph()
# Create network x object form above input
for i, row in nodes.iterrows():
    g.add_node(i, **row)

for _, edge in edges.iterrows():
    g.add_edge(int(edge[0]), int(edge[1]), weight=edge['weight'])


# Should backtranslate network x input into original inptu
def test_networkx_input_conversion():
    nodes_from_nx, edges_from_nx = netplotbrain.utils._from_networkx_input(g, nodecolumnnames=['x', 'y', 'z'], edgecolumnnames=['i', 'j'])
    assert all(nodes_from_nx == nodes)
    assert all(edges_from_nx == edges)

# Should backtranslate network x input into original inptu
@pytest.mark.mpl_image_compare
def test_networkx_input_plot():
    fig, _ = netplotbrain.plot(network=g)
    return fig

