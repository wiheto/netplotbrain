import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .plotting import _plot_template, \
    _plot_edges, _plot_nodes, _plot_spheres,\
    _scale_nodes, _add_axis_arrows, _get_nodes_from_nii, _plot_parcels,\
    _select_single_hemisphere_nodes, _npedges2dfedges, _add_subplot_title, get_frame_input

from .utils import _highlight_nodes, _get_colorby_colors, _set_axes_equal, _get_view


def plot(nodes=None, fig=None, ax=None, view='L', frames=1, edges=None, template=None, templatestyle='filled', templatealpha=0.2,
         templatevoxsize=None, templatecolor='lightgray', surface_resolution=2, templateedgethreshold=0.7, arrowaxis='auto', arrowlength=10,
         arroworigin=None, edgecolor='k', nodesize=1, nodescale=5, nodecolor='salmon', nodetype='spheres', nodecolorby=None,
         nodecmap='Dark2', edgescale=1, edgeweights=True, nodecols='auto', nodeimg=None, nodealpha=1, hemisphere='both', title='auto', highlightnodes=None,
         edgealpha=1, highlightlevel=0.85, edgehighlightbehaviour='both'):
    # sourcery skip: merge-nested-ifs
    """Plot a network on a brain

    Parameters
    ---------------------

    ax : matplotlib ax with 3D projection
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        bnv.plot(ax, ...)
    view : string, list, or tuple
        if string: alternatives are 'A' (anterior), 'P' (posteiror), 'L' (left), 'R' (right), 'I' (inferior), 'S' (superior)
        or any combination of these (e.g 'LR', 'AP')
        The string can contain multiple combinations (e.g. LSR)
        if list: multiple strings (as above) which will create new rows of subplots.
        if tuple: (azim, elev) where azim rotates along xy, and elev rotates along xz.
        If LR or AP view combinations only, you can specify i.e. 'AP-' to rotate in the oposite direction
    nodes : dataframe, string
        The dataframe must include x, y, z columns that correspond to coordinates of nodes (see nodecols to change this).
        Can include additional infomation for node size and color.
        If string, can load a tsv file (tab seperator), assumes index column is the 0th column.
    edges : dataframe, numpy array, or string
        If dataframe, must include i, j columns (and weight, for weighted).
        i and j specify indicies in nodes.
        See edgecols if you want to change the default column names.
        if numpy array, square adjacecny array.
        If string, can load a tsv file (tab seperator), assumes index column is the 0th column.
    template : str or nibabel nifti
        Path to nifti image, or templateflow template name (see templateflow.org) in order to automatically download T1 template.
    templatestyle : str
        can be 'surface': (a surface is rendered from the template),
               'filled': (a single transparant color)
               'cloudy': cloudy (cloudy scatter edges outline the figure)
    surface_resolution : int
        If templatestyle=='surface' controls the size of the triangles used in the surface reconstruction (default: 2).
    templatecolor : str
        If templatestyle=='surface' or 'filled', the color of template voxels
    templateedgedetection : float
        If templatestyle=='cloudy', can tweak the edges detection threshold.
    templatealpha : float
        Opacity of template voxels.
    templatevoxelsize : int
        Resize voxels this size. Larger voxels = quicker. Default = 2
    arrowaxis : list or str
        Adds axis arrows onto plot. Alternatives are: LR, AP, SI, 'all'
    arrowlength : int, float
        Length of arrow
    arroworigin : list
        x,y,z coordinates of arrowaxis. Note 0,0,0 is bottom left.
    edgecolor : matplotlib coloring
        Can be string (default 'black') or list of 3D/4D colors for each edge.
    edgewidth : int, float
        Specify width of edges. If auto, will plot the value in edge array (if array) or the weight column (if in pandas dataframe), otherwise 2.
    edgeweights : string
        String that specifies column in edge dataframe that contains weights.
        If numpy array is edge input, can be True (default) to specify edge weights.
    edgealpha : float
        Transparency of edges.
    nodesize : str, int, float
        If string, can plot a column
    nodecolorby : str
        Column in dataframe that should get different colors (cannot be set with nodecolor)
    nodecmap : str
        Matplotlib colormap for node coloring with nodecolorby.
    nodecolor : matplotlib coloring
        Can be string (default 'black') or list of 3D/4D colors for each edge.
    nodetype : str
        Can be 'spheres', 'circles', or (if nodeimg is specified) 'parcels'.
    nodeimg : str or nii
        String to filename or nibabel object that contains nodes as int.
    nodealpha : float
        Specify the transparency of the nodes
    frames : int
        If specifying 2 views (e.g. LR or AP) and would like to rotates a between them.
        This value will indicate the number of rotations to get from L to R.
        For any other view specification, (e.g. specifying string such as 'LSR')
        then this value is not needed.
    hemisphere: string or list
        If string, can be left or right to specify single hemisphere to include.
        If list, should match the size of views and contain strings to specify hemisphere.
        Can be abbreviated to L, R and (empty string possible if both hemisphere plotted).
        Between hemispehre edges are deleted.
    nodecols : list
        Node column names in node dataframe. 'auto' entails the columsn are ['x', 'y', 'z'] (specifying coordinates)
    edgecols : list
        Edge columns names in edge dataframe. Default is i and j (specifying nodes).
    highlightnodes : int, list, dict
        List or int point out which nodes you want to be highlighted.
        If dict, should be a single column-value pair.
        Example: highlight all nodes of that, in the node dataframe, have a community
        value of 1, the input will be {'community': 1}.
    highlightlevel : float
        Intensity of the highlighting (opposite of alpha).
        Value between 0 and 1, if 1, non-highlighted nodes are fully transparent.
        If 0, non-highlighted nodes are same alpha level as highlighted nodes.
        Default 0.85.
    edgehighlightbehaviour : str
        Alternatives "both" or "any" or None.
        Governs edge dimming when highlightnodes is on
        If both, then highlights only edges between highlighted nodes.
        If any, then only edges connecting any of the nodes are highlighted.


    """
    # Load edge and nodes if string is provided.
    if isinstance(nodes, str):
        nodes = pd.read_csv(nodes, sep='\t', index_col=0)
    if isinstance(edges, str):
        edges = pd.read_csv(edges, sep='\t', index_col=0)
    # set nodecols if no explicit input 
    if nodecols == 'auto':
        nodecols = ['x', 'y', 'z']
    # get the number of views
    if isinstance(view, list):
        nrows = len(view)
    else:
        nrows = 1
        view = [view]
    # If specific views are given, calculate value of frames.
    if len(view[0]) > 2:
        frames = len(view[0])
    n_subplots = nrows * frames
    if ax is not None and not isinstance(ax, list) and n_subplots > 1:
        raise ValueError(
            'Ax input must be a list when requesting multiple frames')
    if isinstance(ax, list):
        if len(ax) != n_subplots:
            raise ValueError('Ax list, must equal number of frames requested')
    # Init figure, if not given as input
    if ax is None:
        fig = plt.figure(figsize=(frames * 3, 3 * nrows))
        colnum = frames * 10
        rows = nrows * 100
    # Check input, if numpy array, make dataframe
    if isinstance(edges, np.ndarray):
        edges = _npedges2dfedges(edges)
    # Set default behaviour of edgeweights
    if edgeweights is None or edgeweights is True:
        edgeweights = 'weight'
    # Load the nifti node file
    if nodeimg is not None:
        nodes, nodeimg = _get_nodes_from_nii(
            nodeimg, voxsize=templatevoxsize, template=template, nodes=nodes)
    # Set nodecolor to colorby argument
    if nodecolorby is not None:
        nodecolor = _get_colorby_colors(nodes, nodecolorby, nodecmap)
    if highlightnodes is not None:
        nodecolor, highlightnodes = _highlight_nodes(nodes, nodecolor, nodealpha, highlightnodes, highlightlevel)
    ax_in = ax
    # Prespecify ouput ax list
    ax_out = []
    # Ax counter for double forloop
    axind = -1
    for ri in range(nrows):
        # Get the azim, elev and arrowaxis for each row
        azim, elev, arrowaxis_row = _get_view(
            view[ri], frames, arrowaxis=arrowaxis)
        for fi in range(frames):
            axind += 1
            # Get hemisphere for this frame
            hemi_frame = get_frame_input(hemisphere, axind, ri, fi)
            # Get title for this frame
            title_frame = get_frame_input(title, axind, ri, fi)
            # Set up subplot
            if ax_in is None:
                subplotid = rows + colnum + axind + 1
                ax = fig.add_subplot(subplotid, projection='3d')
            elif isinstance(ax_in, list):
                # here ax can only be a 1d list, not 2d list.
                ax = ax_in[axind]
            else:
                ax = ax_in

            affine = None
            if template is not None:
                affine = _plot_template(ax, templatestyle, template, templatecolor=templatecolor,
                                        alpha=templatealpha, voxsize=templatevoxsize,
                                        surface_resolution=surface_resolution,
                                        edgethreshold=templateedgethreshold,
                                        azim=azim[fi], elev=elev[fi],
                                        hemisphere=hemi_frame)
            # Template voxels will have origin at 0,0,0
            # It is easier to scale the nodes from the image affine
            # Then to rescale the ax.voxels function
            # So if affine is not None, nodes get scaled in relation to origin and voxelsize,
            # If node coords are derived from nodeimg, this has already been taken care of.
            if nodes is not None and nodeimg is None and axind == 0:
                nodes = _scale_nodes(nodes, affine, nodecols)
            # nodes and subplot may change for each frame/subplot
            # e.g. if hemisphere is specified
            nodes_frame = None
            if nodes is not None:
                nodes_frame = nodes.copy()
                nodes_frame = _select_single_hemisphere_nodes(nodes_frame, affine, hemi_frame, nodecols)

                if nodetype == 'spheres':
                    _plot_spheres(ax, nodes_frame, nodecolor=nodecolor,
                                  nodesize=nodesize, nodecols=nodecols, nodescale=nodescale)
                elif nodetype == 'circles':
                    _plot_nodes(ax, nodes_frame, nodecolor=nodecolor,
                                nodesize=nodesize, nodecols=nodecols)
                elif nodetype == 'parcels':
                    _plot_parcels(ax, nodeimg, alpha=nodealpha,
                                  cmap=nodecolor, parcel_surface_resolution=surface_resolution,
                                  hemisphere=hemi_frame)
            if edges is not None:
                edges_frame = edges.copy()
                _plot_edges(ax, nodes_frame, edges_frame, edgewidth=edgeweights, edgewidthscale=edgescale,
                            edgecolor=edgecolor, edgealpha=edgealpha, highlightnodes=highlightnodes, highlightlevel=highlightlevel,
                            edgehighlightbehaviour=edgehighlightbehaviour)
            if arrowaxis_row is not None:
                _add_axis_arrows(ax, dims=arrowaxis_row,
                                 length=arrowlength, origin=arroworigin,
                                 azim=azim[fi], elev=elev[fi])

            ax.view_init(azim=azim[fi], elev=elev[fi])
            _add_subplot_title(ax, azim[fi], elev[fi], title_frame, hemi_frame)
            # Fix the aspect ratio
            ax.set_box_aspect([1, 1, 1])
            _set_axes_equal(ax)
            ax.axis('off')
            # Append ax to ax_out to store it.
            ax_out.append(ax)

    fig.tight_layout()
    return ax_out
