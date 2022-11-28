from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import matplotlib.pyplot as plt
import templateflow.api as tf

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

nodes['highlight_default'] = nodes['community'] == 'Default'

# test that highlting as a string works
@pytest.mark.mpl_image_compare
def test_highlightnodes_str():
    fig, _ = npbplot(template=None,
            edges=edges,
            nodes=nodes,
            node_color='community',
            node_cmap='inferno',
            highlight_nodes='highlight_default')
    return fig



@pytest.mark.mpl_image_compare
def test_column_as_color():
    atlasinfo = tf.get(template='MNI152NLin2009cAsym',
                   atlas='Schaefer2018',
                   desc='100Parcels7Networks',
                   extension='.tsv')
    atlas_df = pd.read_csv(str(atlasinfo), sep='\t')
    nodes = {'template': 'MNI152NLin2009cAsym',
                      'atlas': 'Schaefer2018',
                      'desc': '100Parcels7Networks',
                      'resolution': 1}
    fig, _ = npbplot(nodes=nodes, node_type='parcels', nodes_df=atlas_df, node_color='color')
    return fig
