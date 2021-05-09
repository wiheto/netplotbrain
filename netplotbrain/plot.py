import numpy as np
from .plotting import _plot_template, \
    _plot_edges, _plot_nodes, _plot_spheres,\
    _scale_nodes, _add_axis_arrows, _plot_parcels,\
    _select_single_hemisphere_nodes, _add_subplot_title, get_frame_input,\
    _setup_legend, _process_edge_input, _process_node_input,\
    _add_nodesize_legend, _add_nodecolor_legend, _init_figure, _check_axinput


from .utils import _highlight_nodes, _get_colorby_colors, _set_axes_equal, _get_view, _load_profile


def plot(nodes=None, fig=None, ax=None, view='L', frames=1, edges=None, template=None, templatestyle='filled', templatealpha=0.2,
         templatevoxsize=None, templatecolor='lightgray', surface_resolution=2, templateedgethreshold=0.7, arrowaxis='auto', arrowlength=10,
         arroworigin=None, edgecolor='k', nodesize=1, nodecolor='salmon', nodetype='circles', nodecolorby=None,
         nodecmap='Dark2', edgescale=1, edgeweights=True, nodecols='auto', nodeimg=None, nodealpha=1, hemisphere='both', title='auto', highlightnodes=None,
         edgealpha=1, highlightlevel=0.85, edgehighlightbehaviour='both', showlegend=True, **kwargs):
    """
    Plot a network on a brain

    Parameters
    ---------------------

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
    nodeimg : str or nii
        String to filename or nibabel object that contains nodes as int.
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
    showlegend : bool or list
        If size or colour have been set, generates a legend for that property at bottom of figure.
        If True, plots all the legends that can be plotted.
        If list, can contain 'nodesize' and 'nodecolor' to plot those in the legend.
        See legend kwargs for turning specific legends on/off.
    nodecolorby : str
        Column in dataframe that should get different colors (cannot be set with nodecolor)
    nodesize : str, int, float
        If string, can plot a column
    title : str or list
        Default auto, will describe the view settings.
        Otherwise string or list of for subplot titles

    NODE KWARGS

    nodecmap : str
        Matplotlib colormap for node coloring with nodecolorby.
    nodecolor : matplotlib coloring
        Can be string (default 'black') or list of 3D/4D colors for each edge.
    nodetype : str
        Can be 'spheres', 'circles', or (if nodeimg is specified) 'parcels'.
    nodealpha : float
        Specify the transparency of the nodes
    nodecols : list
        Node column names in node dataframe. 'auto' entails the columsn are ['x', 'y', 'z'] (specifying coordinates)

    EDGE KWARGS

    edgecols : list
        Edge columns names in edge dataframe. Default is i and j (specifying nodes).
    edgecolor : matplotlib coloring
        Can be string (default 'black') or list of 3D/4D colors for each edge.
    edgewidth : int, float
        Specify width of edges. If auto, will plot the value in edge array (if array) or the weight column (if in pandas dataframe), otherwise 2.
    edgeweights : string
        String that specifies column in edge dataframe that contains weights.
        If numpy array is edge input, can be True (default) to specify edge weights.
    edgealpha : float
        Transparency of edges.
    edgehighlightbehaviour : str
        Alternatives "both" or "any" or None.
        Governs edge dimming when highlightnodes is on
        If both, then highlights only edges between highlighted nodes.
        If any, then only edges connecting any of the nodes are highlighted.

    TEMPLATE KWARGS

    templatecolor : str
        If templatestyle=='surface' or 'filled', the color of template voxels
    templateedgedetection : float
        If templatestyle=='cloudy', can tweak the edges detection threshold.
    templatealpha : float
        Opacity of template voxels.
    templatevoxelsize : int
        Resize voxels this size. Larger voxels = quicker. Default = 2
    surface_resolution : int
        If templatestyle=='surface' controls the size of the triangles used in the surface reconstruction (default: 2).

    LEGENDKWARGS

    nodecolorlegend=True,
    nodesizelegend=True

    ARROW KWARGS

    arrowaxis : list or str
        Adds axis arrows onto plot. Alternatives are: LR, AP, SI, 'all'
    arrowlength : int, float
        Length of arrow
    arroworigin : list
        x,y,z coordinates of arrowaxis. Note 0,0,0 is bottom left.


    FIGURE KWARGS

    ax : matplotlib ax with 3D projection
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        netplotbrain.plot(ax, ...)
    fig : matplotlib figure


    OTHER KWARGS

    profile : str
        path or name of file in netplotbrain/profiles/<filename>.json, specifies default kwargs.
        Default points to netplotbrain/profiles/default.json

    """
    # Load default settings, then update with kwargs
    profile = _load_profile(**kwargs)

    # Check and load the input of nodes and edges
    nodes, nodeimg, nodecols = _process_node_input(
        nodes, nodeimg, nodecols, template, templatevoxsize)
    edges, edgeweights = _process_edge_input(edges, edgeweights)
    # TODO add function for subplot creation here
    # get the number of views
    if isinstance(view, list):
        nrows = len(view)
    else:
        nrows = 1
        view = [view]
    # If specific views are given, calculate value of frames.
    if len(view[0]) > 2:
        frames = len(view[0])
    # Set up legend row
    legends = None
    legendrows = 0
    if isinstance(showlegend, list):
        legends = showlegend
        legendrows = len(legends)
    if showlegend is True:
        # Only plot size legend is sphere/circle and string or list input
        # TODO setup_legend is a little clunky and could be fized
        if nodetype != 'parcel' and not isinstance(nodesize, (float, int)):
            nodesizelegend = profile['nodesizelegend']
            legends = _setup_legend(
                nodesize, nodesizelegend, 'nodesize', legends)
        # Only plot color legend if colorby
        if nodecolorby is not None:
            nodecolorlegend = profile['nodecolorlegend']
            legends = _setup_legend(
                nodecolorby, nodecolorlegend, 'nodecolor', legends)
        if legends is not None:
            legendrows = len(legends)
    # Init figure, if not given as input
    if ax is None:
        fig, gridspec = _init_figure(frames, nrows, legendrows)
    else:
        expected_ax_len = (nrows * frames) + legendrows
        _check_axinput(ax, expected_ax_len)
    # Set nodecolor to colorby argument
    if nodecolorby is not None:
        nodecolor = _get_colorby_colors(nodes, nodecolorby, nodecmap)
    if highlightnodes is not None:
        nodecolor, highlightnodes = _highlight_nodes(
            nodes, nodecolor, nodealpha, highlightnodes, highlightlevel)
    ax_in = ax
    # Prespecify ouput ax list
    ax_out = []
    # TODO remove double forloop and make single forloop by running over nrows and frames
    for ri in range(nrows):
        # Get the azim, elev and arrowaxis for each row
        azim, elev, arrowaxis_row = _get_view(
            view[ri], frames, arrowaxis=arrowaxis)
        for fi in range(frames):
            axind = (ri * nrows) + fi
            # Get hemisphere for this frame
            hemi_frame = get_frame_input(hemisphere, axind, ri, fi)
            # Get title for this frame
            title_frame = get_frame_input(title, axind, ri, fi)
            # Set up subplot
            if ax_in is None:
                ax = fig.add_subplot(gridspec[ri, fi], projection='3d')
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
                nodes = _scale_nodes(nodes, nodecols, affine)
            # nodes and subplot may change for each frame/subplot
            # e.g. if hemisphere is specified
            nodes_frame = None
            if nodes is not None:
                nodes_frame = nodes.copy()
                nodes_frame = _select_single_hemisphere_nodes(
                    nodes_frame, nodecols[0], affine, hemi_frame)

                if nodetype == 'spheres':
                    _plot_spheres(ax, nodes_frame, nodecolor=nodecolor,
                                  nodesize=nodesize, nodecols=nodecols, **profile)
                elif nodetype == 'circles':
                    _plot_nodes(ax, nodes_frame, nodecolor=nodecolor,
                                nodesize=nodesize, nodecols=nodecols, **profile)
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
    # Add legends to plot
    if legends is not None:
        for li, legend in enumerate(legends):
            # setup legend subplot. Goes in centre or centre2 subplots
            spind = gridspec.ncols
            if np.remainder(spind, 2) == 0:
                legend_subplotp_colind = [int((spind / 2) - 1), int(spind / 2)]
            else:
                legend_subplotp_colind = int(np.round(spind / 2) - 1)
            ax = fig.add_subplot(gridspec[nrows + li, legend_subplotp_colind])

            if legend == 'nodesize':
                ax = _add_nodesize_legend(ax, nodes, nodesize, **profile)
            if legend == 'nodecolor':
                ax = _add_nodecolor_legend(
                    ax, nodes, nodecolorby, nodecolor, **profile)
            ax.axis('off')
            #ax = _add_size_legend(ax, nodes, nodesize, nodescale)
            ax_out.append(ax)
    fig.tight_layout()

    return ax_out
