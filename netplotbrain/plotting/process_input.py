import pandas as pd
import numpy as np
from ..plotting import _npedges2dfedges, _get_nodes_from_nii

def get_frame_input(inputvar, axind, ri, fi):
    """
    Gets subplot varible.

    The variable depends on whether the
    input is a string, array or 2d array.
    """
    if isinstance(inputvar, str):
        var_frame = inputvar
    elif isinstance(inputvar[0], str):
        var_frame = inputvar[axind]
    else:
        var_frame = inputvar[ri][fi]
    return var_frame

def _process_node_input(nodes, nodeimg, nodecols, template, templatevoxsize): 
    """
    Takes node input (nodes, nodeimg and nodecols) and processes them.
    Loads pandas dataframe if nodes is string.
    Gets the nodes from the nifti file if nodeimg is set.
    Sets defult columns for nodecols. 
    """
    # Load nodes if string is provided
    if isinstance(nodes, str):
        nodes = pd.read_csv(nodes, sep='\t', index_col=0)
    # Load the nifti node file
    if nodeimg is not None:
        nodes, nodeimg = _get_nodes_from_nii(
            nodeimg, voxsize=templatevoxsize, template=template, nodes=nodes)
    # set nodecols if no explicit input
    if nodecols == 'auto':
        nodecols = ['x', 'y', 'z']
    return nodes, nodeimg, nodecols

def _process_edge_input(edges, edgeweights):
    """
    Takes the input edges and edgeweight.
    Loads pandas dataframe if edges is string.
    Creates pandas dataframe if edges is numpy array.
    Sets defauly edgeweight to "weight" if not given. 
    """
    if isinstance(edges, str):
        edges = pd.read_csv(edges, sep='\t', index_col=0)
    # Check input, if numpy array, make dataframe
    if isinstance(edges, np.ndarray):
        edges = _npedges2dfedges(edges)
    # Set default behaviour of edgeweights
    if edgeweights is None or edgeweights is True:
        edgeweights = 'weight'
    return edges, edgeweights