from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import numpy as np

# Example node and edges dataframes included with package
df_adj = pd.read_csv('./examples/nbstestdata.csv', index_col=[0])

# Simplest image
@pytest.mark.mpl_image_compare
def test_highlight_edges_df():
    fig, _ = npbplot(nodes={'atlas': 'Schaefer2018',
                                        'desc': '100Parcels7Networks',
                                        'resolution': 1},
                                edges=df_adj,
                                highlight_edges='nbs',
                                template='MNI152NLin2009cAsym',
                                template_style='glass',
                                view=['LSR'],
                                title='NBS integration',
                                node_type='circles',
                                highlightlevel=0.5)
    return fig


N = df_adj[['i', 'j']].max().max() + 1
adj = np.zeros([N, N])
adj[df_adj['i'], df_adj['j']] = df_adj['weight']
thadj = np.array(adj)
thadj[thadj<0.5] = 0
thadj[thadj!=0] = 1
@pytest.mark.mpl_image_compare
def test_highlight_edges_np():
    fig, _ = npbplot(nodes={'atlas': 'Schaefer2018',
                                        'desc': '100Parcels7Networks',
                                        'resolution': 1},
                                edges=adj,
                                highlight_edges=thadj,
                                template='MNI152NLin2009cAsym',
                                template_style='glass',
                                view=['LSR'],
                                title='NBS integration',
                                node_type='circles',
                                highlightlevel=0.5)
    return fig
