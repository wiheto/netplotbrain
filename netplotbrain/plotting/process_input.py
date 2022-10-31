import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..plotting import _npedges2dfedges, _get_nodes_from_nii

def get_frame_input(inputvar, axind, ri, fi, nrows, frames):
    """
    Gets subplot variable.

    The variable depends on whether the
    input is a string, array or 2d array.
    """
    # First sett if input is a singular string, int or None.
    if isinstance(inputvar, int):
        var_frame = inputvar
    elif isinstance(inputvar, str):
        var_frame = inputvar
    elif inputvar is None:
        var_frame = inputvar
    # Then check if first input of list is also a list (e.g. format ['LR', 'SP'])
    elif len(inputvar) == nrows and isinstance(inputvar[0], str) and len(inputvar[0]) == frames:
        var_frame = inputvar[ri][fi]
    # If a 2x2 figure input is ['LRSP']
    elif len(inputvar) == (nrows * frames):
        var_frame = inputvar[axind]
    else:
        var_frame = inputvar[ri][fi]
    return var_frame


def _process_node_input(nodes, nodes_df, node_color, node_columnnames, template, template_voxelsize):
    """
    Takes node input (nodes, nodesdf and node_columnnames) and processes them.
    Loads pandas dataframe if nodes is string.
    Gets the nodes from the nifti file if nodes is an img is set.
    Sets defult columns for node_columnnames.
    If nodes is an img, then nodes_df passes additional info if wanted.
    """
    # Preset nodeimg to None
    nodeimg=None
    # Load nodes if string is provided
    if isinstance(nodes, pd.DataFrame) or nodes is None:
        pass
    elif isinstance(nodes, str):
        if nodes.endswith('.tsv'):
            nodes = pd.read_csv(nodes, sep='\t', index_col=0)
        elif nodes.endswith('.csv'):
            nodes = pd.read_csv(nodes, index_col=0)
        elif nodes.endswith('.nii') or  nodes.endswith('.nii.gz'):
            nodes, nodeimg = _get_nodes_from_nii(
                nodes, voxsize=template_voxelsize, template=template, nodes=nodes_df)
        else:
            raise ValueError('nodes as str must be a .csv, .tsv, .nii, or .nii.gz')
    else:
        nodes, nodeimg = _get_nodes_from_nii(
            nodes, voxsize=template_voxelsize, template=template, nodes=nodes_df)
    # set node_columnnames if no explicit input
    if node_columnnames == 'auto':
        node_columnnames = ['x', 'y', 'z']
    # Check if node_color is a string in nodes, if yes, set to node_colorby to node_color
    # Note: this may not be the most effective way to do this.
    node_colorby = None
    if isinstance(node_color, str) and nodes is not None:
        if node_color in nodes:
            node_colorby = str(node_color)
    return nodes, nodeimg, node_colorby, node_columnnames


def _process_edge_input(edges, edge_weights, **kwargs):
    """
    Takes the input edges and edgeweight.
    Loads pandas dataframe if edges is string.
    Creates pandas dataframe if edges is numpy array.
    Sets default edgeweight to "weight" if not given.
    """
    edge_threshold = kwargs.get('edge_threshold')
    edge_thresholddirection = kwargs.get('edge_thresholddirection')
    edges_df = kwargs.get('edges_df')
    if isinstance(edges, str):
        edges = pd.read_csv(edges, sep='\t', index_col=0)
    # Check input, if numpy array, make dataframe
    if isinstance(edges, np.ndarray):
        edges = _npedges2dfedges(edges)
        edge_weights = 'weight'
    # Merge edges_df if it exists.
    if edges_df is not None:
        edges = edges.merge(edges_df, how='left')
    # Set default behaviour of edge_weights
    if isinstance(edges, pd.DataFrame):
        if edge_weights is None or edge_weights is True:
            edge_weights = 'weight'
        if 'weight' not in edges:
            edge_weights = None
        if edge_weights is not None and edge_weights not in edges:
            raise ValueError('edge_weights is specified and not in edges')
        # If edgeweight and edge_threshold have been set
        if edge_weights is not None and edge_threshold is not None:
            if edge_thresholddirection == 'absabove':
                edges = edges[np.abs(edges[edge_weights]) > edge_threshold]
            if edge_thresholddirection == 'above' or edge_thresholddirection == '>':
                edges = edges[edges[edge_weights] > edge_threshold]
            if edge_thresholddirection == 'below' or edge_thresholddirection == '<':
                edges = edges[edges[edge_weights] < edge_threshold]

    return edges, edge_weights


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


def _process_highlightedge_input(edges, highlight_edges, **profile):
    # if highlight edges is array, convert to pandas.
    if isinstance(highlight_edges, np.ndarray):
        # Convert np input to pd
        highlight_edges = _npedges2dfedges(highlight_edges)
        ecols = profile['edge_columnnames']
        # Make sure that the i and j column are the same name
        # Also rename weight to edge_to_highlight
        highlight_edges.rename(columns = {'weight': 'edge_to_highlight',
                                         'i': ecols[0],
                                         'j': ecols[1]}, inplace = True)
        # Merge dataframes with edges
        edges = edges.merge(highlight_edges, how='left')
        # Make nans 0s
        edges['edge_to_highlight'] = edges['edge_to_highlight'].fillna(0)
        # Rename highlight_edges to new column
        highlight_edges = 'edge_to_highlight'
    return edges, highlight_edges