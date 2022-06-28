from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import numpy as np

# Example node and edges dataframes included with package
df_adj = pd.read_csv('./examples/nbstestdata.csv', index_col=[0])

# Simplest image
@pytest.mark.mpl_image_compare
def test_highlightedges_df():
    fig, _ = npbplot(nodes={'atlas': 'Schaefer2018',
                                        'desc': '100Parcels7Networks',
                                        'resolution': 1},
                                edges=df_adj,
                                highlightedges='nbs',
                                template='MNI152NLin2009cAsym',
                                templatestyle='glass',
                                view=['LSR'],
                                title='NBS integration',
                                nodetype='circles',
                                highlightlevel=0.5)
    return fig


N = df_adj[['i', 'j']].max().max() + 1
adj = np.zeros([N, N])
adj[df_adj['i'], df_adj['j']] = df_adj['weight']
thadj = np.array(adj)
thadj[thadj<0.5] = 0
thadj[thadj!=0] = 1
@pytest.mark.mpl_image_compare
def test_highlightedges_np():
    fig, _ = npbplot(nodes={'atlas': 'Schaefer2018',
                                        'desc': '100Parcels7Networks',
                                        'resolution': 1},
                                edges=adj,
                                highlightedges=thadj,
                                template='MNI152NLin2009cAsym',
                                templatestyle='glass',
                                view=['LSR'],
                                title='NBS integration',
                                nodetype='circles',
                                highlightlevel=0.5)
    return fig
