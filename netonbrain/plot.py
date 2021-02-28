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
    view : string or tuple
        if string: alternatives are 'A' (anterior), 'P' (posteiror), 'L' (left), 'R' (right), 'I' (inferior), 'S' (superior)
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

    azim, elev, arrowaxis = _get_view(view, frames, arrowaxis=arrowaxis)
    if ax is not None and not isinstance(ax, list) and len(azim) > 1:
        raise ValueError(
            'Ax input must be a list when requesting multiple frames')
    if isinstance(ax, list):
        if len(ax) != len(azim):
            raise ValueError('Ax list, must equal number of frames requested')
    if ax is None:
        fig = plt.figure(figsize=(len(azim)*3, 3))
        colnum = len(azim) * 10

    ax_in = ax
    ax_out = []
    for fi, _ in enumerate(azim):
        if ax_in is None:
            subplotid = 100 + colnum + fi + 1
            ax = fig.add_subplot(subplotid, projection='3d')
        else:
            ax = ax_in[fi]

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
        if fi == 0:
            nodes = _scale_nodes(nodes, affine)
        if edges is not None:
            _plot_edges(ax, nodes, edges, edgewidth=edgewidth,
                        edgecolor=edgecolor)
        if nodes is not None:
            if nodespheres:
                _plot_spheres(ax, nodes, nodecolor=nodecolor, nodesize=nodesize, nodecols=nodecols, nodescale=nodescale)
            else:
                _plot_nodes(ax, nodes, nodecolor=nodecolor, nodesize=nodesize, nodecols=nodecols)
        if arrowaxis is not None:
            _add_axis_arrows(ax, dims=arrowaxis,
                             length=arrowlength, origin=arroworigin,
                             azim=azim[fi], elev=elev[fi])

        ax.set_box_aspect([1, 1, 1])  # IMPORTANT - this is the new, key line
        _set_axes_equal(ax)  # IMPORTANT - this is also required
        ax.axis('off')
        ax.view_init(azim=azim[fi], elev=elev[fi])
        ax_out.append(ax)
        fig.tight_layout()
    return ax_out
