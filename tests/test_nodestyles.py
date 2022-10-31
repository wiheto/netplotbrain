from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import numpy as np

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# Create an edge array input as well
nnodes = edges[['i', 'j']].max().max() + 1
edge_array = np.zeros([nnodes, nnodes])
edge_array[edges['i'].values, edges['j'].values] = 1

@pytest.mark.mpl_image_compare
def test_cont_colormap():
    fig, _ = npbplot(template=None,
                      view='S',
                      nodes=nodes,
                      nodesize=40,
                      edges=edges,
                      node_cmap='RdBu',
                      nodecolor='centrality_measure1',
                      node_colorlegendstyle='continuous')
    return fig

@pytest.mark.mpl_image_compare
def test_nodevminvmax():
    fig, _ = npbplot(template=None,
                      view='S',
                      node_scale=100,
                      nodes=nodes,
                      nodesize='centrality_measure1',
                      edges=edges,
                      node_cmap='RdBu',
                      node_sizevminvmax=[0.6, 1.1])
    return fig

# Nodes as spheres
@pytest.mark.mpl_image_compare
def test_spheres():
    fig, _ = npbplot(nodes=nodes,
                  edges=edge_array,
                  template='MNI152NLin2009cAsym',
                  template_style=None,
                  view=['A'],
                  nodetype='spheres',
                  node_alpha=0.5,
                  nodecolor='Salmon',
                  title='Sphere test')
    return fig
