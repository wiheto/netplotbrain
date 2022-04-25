import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..plotting import _npedges2dfedges, _get_nodes_from_nii

def get_frame_input(inputvar, axind, ri, fi, exnotlist=True):
    """
    Gets subplot variable.

    The variable depends on whether the
    input is a string, array or 2d array.
    """
    if exnotlist:
        if not isinstance(inputvar, list):
            var_frame = inputvar
        elif not isinstance(inputvar[0], list):
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


def _process_edge_input(edges, edgeweights, **kwargs):
    """
    Takes the input edges and edgeweight.
    Loads pandas dataframe if edges is string.
    Creates pandas dataframe if edges is numpy array.
    Sets default edgeweight to "weight" if not given.
    """
    edgethreshold = kwargs.get('edgethreshold')
    edgethresholddirection = kwargs.get('edgethresholddirection')
    if isinstance(edges, str):
        edges = pd.read_csv(edges, sep='\t', index_col=0)
    # Check input, if numpy array, make dataframe
    if isinstance(edges, np.ndarray):
        edges = _npedges2dfedges(edges)
        edgeweights = 'weight'
    # Set default behaviour of edgeweights
    if isinstance(edges, pd.DataFrame):
        if edgeweights is None or edgeweights is True:
            edgeweights = 'weight'
        if 'weight' not in edges:
            edgeweights = None
        if edgeweights is not None and edgeweights not in edges:
            raise ValueError('Edgeweights is specified and not in edges')
        # If edgeweight and edgethreshold have been set
        if edgeweights is not None and edgethreshold is not None:
            if edgethresholddirection == 'absabove':
                edges = edges[np.abs(edges[edgeweights]) > edgethreshold]
            if edgethresholddirection == 'above' or edgethresholddirection == '>':
                edges = edges[edges[edgeweights] > edgethreshold]
            if edgethresholddirection == 'below' or edgethresholddirection == '<':
                edges = edges[edges[edgeweights] < edgethreshold]
            
    return edges, edgeweights


def _init_figure(frames, nrows, legendrow):
    widths = [6] * frames
    heights = [6] * nrows
    if legendrow > 0:
        heights += [1] * legendrow
    fig = plt.figure(figsize=(frames * 3, (3 * nrows) + (0.5 * legendrow)))
    gridspec = fig.add_gridspec(ncols=frames,
                                nrows=nrows+legendrow,
                                width_ratios=widths,
                                height_ratios=heights)
    return fig, gridspec

def _check_axinput(ax, expected_ax_len):
    if not isinstance(ax, list) and expected_ax_len > 1:
        raise ValueError(
            'Ax input must be a list when requesting multiple frames')
    if isinstance(ax, list):
        if len(ax) != expected_ax_len:
            raise ValueError('Ax list, must equal number of frames requested')
    if not isinstance(ax, list):
        ax = [ax]
    gridspec = ax[0].get_gridspec()
    return ax, gridspec

