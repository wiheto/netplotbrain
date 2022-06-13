import pandas as pd
from netplotbrain import plot as npbplot
import pytest
import templateflow.api as tf

# Download atlas info
atlasinfo = tf.get(template='MNI152NLin2009cAsym',
                   atlas='Schaefer2018',
                   desc='100Parcels7Networks',
                   extension='.tsv')
atlasinfo = pd.read_csv(atlasinfo, sep='\t')
# Parse the info in to get network names
networks = list(map(lambda x: x.split('_')[2], atlasinfo.name.values))
atlasinfo['yeo7networks'] = networks


@pytest.mark.mpl_image_compare
def test_templateflow_atlas_highlight():
    fig, _ = npbplot(nodes_df=atlasinfo,
                      nodes={'atlas': 'Schaefer2018',
                               'desc': '100Parcels7Networks',
                               'resolution': 1},
                      template='MNI152NLin2009cAsym',
                      templatestyle=None,
                      view=['L'],
                      nodetype='parcels',
                      nodecolor='Dark2',
                      nodecolorby='yeo7networks',
                      nodealpha=0.8,
                      title='Highlight a community',
                      highlightnodes={'yeo7networks': 'Cont'},
                      highlightlevel=0.95,
                      nodecolorlegend=False,
                      nodesizelegend=False)
    return fig
