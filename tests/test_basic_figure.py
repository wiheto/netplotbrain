import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt
import pytest

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

print('this ran')
# Plot single view
def test_simple(plt):
    netplotbrain.plot(template='MNI152NLin2009cAsym',
                    templatestyle='surface',
                    view='S',
                    nodes=nodes,
                    nodescale=40,
                    nodesize='centrality_measure1',
                    edges=edges,
                    nodecolorby='community')
    plt.saveas = "test_plot.png"

    assert 1 == 1