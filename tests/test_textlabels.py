#%%
import pandas as pd
import numpy as np
import netplotbrain
import templateflow.api as tf
import itertools
import pytest
import matplotlib.pyplot as plt


#%%
@pytest.mark.mpl_image_compare
def test_labels():
        #%%
        atlas = {'template': 'MNI152NLin2009cAsym',
                'atlas': 'Schaefer2018',
                'desc': '100Parcels7Networks'}
        atlasinfo = tf.get(extension='.tsv', **atlas)
        atlasinfo = pd.read_csv(atlasinfo, sep='\t')
        # Parse the info in to get network names
        atlasinfo['label'] = np.arange(1, 101)

        atlasinfo['label'].loc[0] = None
        atlas['resolution'] = 1

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        netplotbrain.plot(template='MNI152NLin2009cAsym',
                        fig = fig,
                        ax = ax,
                        nodes=atlas,
                        nodes_df=atlasinfo,
                        node_style = 'circles',
                        node_text='label',
                        node_text_style='center',
                        view='S', 
                        template_style='glass',
                        node_scale=20,
                        seed=2022,
                        title=None,
                        subtitle=None)
        return fig


    # %%
