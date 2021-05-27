import pandas as pd
from netplotbrain import plot as npbplot

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

def test_simple():
    fig, ax = npbplot(template='MNI152NLin2009cAsym',
            templatestyle='surface',
            view='S',
            nodes=nodes,
            nodescale=40,
            nodesize='centrality_measure1',
            edges=edges,
            nodecolorby='community')
    # Dummy test for now
    assert 1 == 1
