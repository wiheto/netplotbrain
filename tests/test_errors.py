from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# Expected value errors

# If nodes and network are specified together
def test_error_network_and_node_input():
    with pytest.raises(ValueError):
        npbplot(template=None,
                edges=None,
                nodes=1,
                network=1)


# If network is not nx
def test_error_network_not_nx():
    with pytest.raises(ValueError):
        npbplot(template=None,
                edges=None,
                nodes=None,
                network=1)

# If highlightedges and highlightnods are specified at the same time
def test_error_doublehighlight():
    with pytest.raises(ValueError):
        npbplot(template=None,
                edges=edges,
                nodes=nodes,
                highlight_edges=1,
                highlight_nodes=1,)
