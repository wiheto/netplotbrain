from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# Simplest image
@pytest.mark.mpl_image_compare
def test_simple():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      templatestyle='surface',
                      view='S',
                      nodes=nodes,
                      nodescale=40,
                      nodesize='centrality_measure1',
                      edges=edges,
                      nodecolorby='community')
    return fig


# Only plot a single hemisephere
@pytest.mark.mpl_image_compare
def test_singlehemisphere():
    fig, _ = npbplot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['SSS'],
                  hemisphere=['L', 'R', ''],
                  nodealpha=0.5,
                  nodecolor='Salmon')
    return fig

# Figure that receives own ax
def test_customax():
    fig = plt.figure()
    ax = []
    for axind in range(3):
        ax.append(fig.add_subplot(231+axind, projection='3d'))
    fig, _ = npbplot(template=None,
                      view=['SLP'],
                      nodes=nodes,
                      nodescale=40,
                      nodesize='centrality_measure1',
                      edges=edges,
                      fig=fig,
                      ax=ax)
    return fig