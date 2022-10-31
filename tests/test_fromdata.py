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
                      template_style='glass',
                      view='S',
                      nodes=nodes,
                      node_scale=40,
                      nodesize='centrality_measure1',
                      edges=edges,
                      nodecolor='community')
    return fig


# Only plot a single hemisephere
@pytest.mark.mpl_image_compare
def test_singlehemisphere():
    fig, _ = npbplot(nodes=nodes,
                  edges=edges,
                  template='MNI152NLin2009cAsym',
                  template_style=None,
                  view=['SSS'],
                  hemisphere=['L', 'R', ''],
                  node_alpha=0.5,
                  nodecolor='Salmon')
    return fig

# Figure that receives own ax
@pytest.mark.mpl_image_compare
def test_customax():
    fig = plt.figure()
    ax = []
    for axind in range(3):
        ax.append(fig.add_subplot(231+axind, projection='3d'))
    fig, _ = npbplot(template=None,
                      view=['SLP'],
                      nodes=nodes,
                      node_scale=40,
                      nodesize='centrality_measure1',
                      edges=edges,
                      fig=fig,
                      ax=ax)
    return fig

# Test gif plot
def test_gif_plot():
    fig, _ = npbplot(template=None,
                      view=['AP'],
                      frames=3,
                      nodes=nodes,
                      node_scale=40,
                      nodesize='centrality_measure1',
                      edges=edges,
                      gif=True,
                      savename='giftest')
    return fig