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

# Simplest image


@pytest.mark.mpl_image_compare
def test_simple():
    fig, ax = npbplot(template='MNI152NLin2009cAsym',
                      templatestyle='surface',
                      view='S',
                      nodes=nodes,
                      nodescale=40,
                      nodesize='centrality_measure1',
                      edges=edges,
                      nodecolorby='community')
    return fig

# Nodes as spheres


@pytest.mark.mpl_image_compare
def test_spheres():
    fig, ax = npbplot(nodes=nodes,
                  edges=edge_array,
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['A'],
                  nodetype='spheres',
                  nodealpha=0.5,
                  nodecolor='Salmon',
                  title='Sphere test')
    return fig
