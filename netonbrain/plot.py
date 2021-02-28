import matplotlib.pyplot as plt
import inspect
from .plotting import _plot_template, _plot_template_style_filled, _plot_template_style_cloudy,\
    _plot_edges, _plot_nodes, _plot_spheres, _set_axes_equal, _set_axes_radius, _get_view,\
    _scale_nodes, _add_axis_arrows, _plot_template_style_surface


def plot(nodes, fig=None, ax=None, view='L', frames=1, edges=None, template=None, templatestyle='filled', templatealpha=0.2,
         templatevoxsize=2, templatecolor='lightgray', surface_resolution=2, templateedgethreshold=0.7, arrowaxis='auto', arrowlength=10,
         arroworigin=None, edgecolor='k', edgewidth='auto', nodesize=1, nodescale=5, nodecolor='salmon', nodespheres=True,
         weightcol='weights', nodecols=['x', 'y', 'z']):
    # sourcery skip: merge-nested-ifs
    """
    Plot a network on a brain

    Parameters
    ---------------------

    ax : matplotlib ax with 3D projection
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        bnv.plot(ax, ...)
    view : string, list, or tuple
        if string: alternatives are 'A' (anterior), 'P' (posteiror), 'L' (left), 'R' (right), 'I' (inferior), 'S' (superior)
        or any combination of these (e.g 'LR', 'AP')
        if list: multiple strings (as above) which will create new rows of subplots.
        if tuple: (azim, elev) where azim rotates along xy, and elev rotates along xz.
    nodes : dataframe
        must include x, y, z columns that correspond to coordinates of nodes. Can include additional infomation for node size and color.
    edges : numpy array (other alternatives coming)
        if numpy array, square adjacecny array.
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
    nodesize : str, int, float
        If string, can plot a column
    nodecolor : matplotlib coloring
        Can be string (default 'black') or list of 3D/4D colors for each edge.
    nodespheres : bool
        If True, plots nodes as 3D spheres. If False, plots nodes as flat circles. Flat circles can be quicker.

    """

    # get the number of views
    if isinstance(view, list):
        nrows = len(view)
    else:
        nrows = 1
        view = [view]
    n_subplots = nrows * frames
    if ax is not None and not isinstance(ax, list) and n_subplots > 1:
        raise ValueError(
            'Ax input must be a list when requesting multiple frames')
    if isinstance(ax, list):
        if len(ax) != n_subplots:
            raise ValueError('Ax list, must equal number of frames requested')
    if ax is None:
        fig = plt.figure(figsize=(frames * 3, 3 * nrows))
        colnum = frames * 10
        rows = nrows * 100

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
            if ax_in is None:
                subplotid = rows + colnum + axind + 1
                ax = fig.add_subplot(subplotid, projection='3d')
            else:
                # here ax can only be a 1d list, not 2d list.
                ax = ax_in[axind]

            affine = None
            if template is not None:
                affine = _plot_template(ax, templatestyle, template, templatecolor=templatecolor,
                                        alpha=templatealpha, voxsize=templatevoxsize,
                                        surface_resolution=surface_resolution,
                                        edgethreshold=templateedgethreshold,
                                        azim=azim[fi], elev=elev[fi])
            # Template voxels will have origin at 0,0,0
            # It is easier to scale the nodes from the image affine
            # Then to rescale the ax.voxels function
            # So if affine is not None, nodes get scaled in relation to origin and voxelsize,
            if axind == 0:
                nodes = _scale_nodes(nodes, affine)
            if edges is not None:
                _plot_edges(ax, nodes, edges, edgewidth=edgewidth,
                            edgecolor=edgecolor)
            if nodes is not None:
                if nodespheres:
                    _plot_spheres(ax, nodes, nodecolor=nodecolor,
                                  nodesize=nodesize, nodecols=nodecols, nodescale=nodescale)
                else:
                    _plot_nodes(ax, nodes, nodecolor=nodecolor,
                                nodesize=nodesize, nodecols=nodecols)
            if arrowaxis_row is not None:
                _add_axis_arrows(ax, dims=arrowaxis_row,
                                 length=arrowlength, origin=arroworigin,
                                 azim=azim[fi], elev=elev[fi])

            # IMPORTANT - this is the new, key line
            ax.set_box_aspect([1, 1, 1])
            _set_axes_equal(ax)  # IMPORTANT - this is also required
            ax.axis('off')
            ax.view_init(azim=azim[fi], elev=elev[fi])
            ax_out.append(ax)

    fig.tight_layout()
    return ax_out
