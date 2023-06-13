import pandas as pd
import numpy as np
from bids import BIDSLayout 
import itertools
import os

def generate_group_cm(nodes, subjects, community_size, community_str, scale=0.25, seed=2022):
    """
    Quick way to simulate group differences for visualization purposes.

    Input
    -----
    nodes : int
        number of nodes
    subjects : int
        number of subjects
    community_size : list
        list of number of nodes in each community
    community_str : list
        list of mean str for within community connections
    scale : float
        scale (STD) of normal distribution.
    """
    np.random.seed(seed)
    mu = np.zeros([nodes, nodes, 1])
    np.fill_diagonal(mu[:, :, 0], 1)
    ci = 0
    for i, c in enumerate(community_size):
        mu[ci:ci+c, ci:ci+c, :] = community_str[i]
        ci += c

    # Simulate data
    g = np.random.normal(mu, scale, size=[nodes, nodes, subjects])
    # Force to be symmetric
    ind_i, ind_j = np.triu_indices(g.shape[0], k=1)
    g[ind_j, ind_i] = g[ind_i, ind_j]
    return g

# To be run in data directory
layout = BIDSLayout('./')
# Specify variable for generating data
nodes = 100
subjects_per_group = 3
#
# Make a numpy array with four different rows with different connectivity vectors 
community_str = np.array([[0.2, 0.1, 0.2, 0.1],
                          [0.2, 0.1, 0.1, 0.2],
                          [0.1, 0.2, 0.2, 0.1],
                          [0.1, 0.2, 0.1, 0.2]])
community_size = [25, 25, 25, 25]

output_pattern = './sub-{subject}/ses-{session}/{datatype}/'
output_fname = output_pattern + 'sub-{subject}_ses-{session}_task-{task}_relmat.tsv'
   
subjects = ['001', '002', '003']
combinations = itertools.product(['a', 'b'], ['pre', 'post'])
for i, (task, session) in enumerate(combinations):
    g = generate_group_cm(nodes, subjects_per_group, community_size, community_str[i, :])
    for j, s in enumerate(subjects):
        df = pd.DataFrame(g[:, :, j])
        entities = {'subject': s,
                    'task': task,
                    'session': session,
                    'datatype': 'func'}
        out_dirs = layout.build_path(entities, path_patterns=output_pattern, validate=False)
        output_path = layout.build_path(entities, path_patterns=output_fname, validate=False)
        os.makedirs(out_dirs, exist_ok=True)
        df.to_csv(output_path, sep='\t')
