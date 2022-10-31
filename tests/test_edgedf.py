from netplotbrain import plot as npbplot
import pytest
import pandas as pd
import numpy as np

# Create 100 random edges. Setting negative ones to 0 for simplicity
np.random.seed(2022)
xtriu, ytriu = np.triu_indices(100, k=1)
weights = np.random.normal(-.5, 0.5, len(xtriu))
graph = np.zeros([100, 100])
graph[xtriu, ytriu] = weights
graph[ytriu, xtriu] = weights
graph[graph<0] = 0

# Create additional edge dataframe
col = np.ones(len(xtriu))
col[1500:] = 2
col[2500:] = 3
col[3500:] = 4

edges_df = pd.DataFrame(data={'i': xtriu, 'j': ytriu, 'color': col})

@pytest.mark.mpl_image_compare
def test_edges_df():
    fig, _ = npbplot(nodes={'atlas': 'Schaefer2018',
                                        'desc': '100Parcels7Networks',
                                        'resolution': 1},
                                edges=graph,
                                edges_df=edges_df,
                                template='MNI152NLin2009cAsym',
                                template_style='glass',
                                view=['S'],
                                edgecolor='color',
                                title='Edge_df',
                                nodetype='circles',
                                edge_cmap='tab10',
                                edge_threshold=0,
                                edge_widthscale=5,
                                edge_thresholddirection='above')
    return fig
