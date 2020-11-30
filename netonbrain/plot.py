import matplotlib.pyplot as plt
from .plotting import _plot_template, _plot_template_style_filled, _plot_template_style_glass,\
                    _plot_edges, _plot_nodes, _set_axes_equal, _set_axes_radius, _get_view,\
                    _scale_nodes, _add_axis_arrows
                    


def plot(nodes, fig=None, ax=None, view='L', frames=1, edges=None, template=None, templatestyle='filled', templatealpha=0.2,
        templatevoxsize=4, templatecolor='lightgray', templateedgedetection=0.8, arrowaxis='auto', arrowlength=5,
        arroworigin=[5, 5, 5], edgecolor='k', edgewidth='auto', nodesize=50, nodecolor='salmon'):
    # sourcery skip: merge-nested-ifs
    """
    Plot a network on a brain

    ax : matplotlib ax with 3D projection
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        bnv.plot(ax, ...)
    view : string or tuple
        if string: alternatives are 'A' (anterior), 'P' (posteiror), 'L' (left), 'R' (right), 'D' (dorsal), 'V' (ventral)
        if tuple: (azim, elev) where azim rotates along xy, and elev rotates along xz.  
    nodes : dataframe
        must include x, y, z columns that correspond to coordinates of nodes. Can include additional infomation for node size and color.
    edges : numpy array (other alternatives coming)
        if numpy array, square adjacecny array.
    template : str or nibabel nifti
        Path to nifti image, or templateflow template name (see templateflow.org) in order to automatically download T1 template.
    templatestyle : str
        can be filled (a single transparant color) or glass (edges marked)
    templatecolor : str
        If templatestyle=='filled', the color of template voxels
    templateedgedetection : float 
        If templatestyle=='glass', can tweak the edges of 
    templatealpha : float
        Opacity of template voxels. 
    templatevoxelsize : int
        Resize voxels this size. Larger voxels = quicker. 
    arrowaxis : list or str
        Adds axis arrows onto plot. Alternatives are: LR, AP, DV, 'all'
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
    azim : int
        angle to inital view
    elev : int
        elevation of initial view,
    """

    azim, elev, arrowaxis = _get_view(view, frames, arrowaxis=arrowaxis)
    if ax is not None and not isinstance(ax, list) and len(azim) > 1:
        raise ValueError('Ax input must be a list when requesting multiple frames')
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
            affine = _plot_template(ax, templatestyle, template, templatecolor=templatecolor, alpha=templatealpha, voxsize=templatevoxsize, azim=azim[fi], elev=elev[fi])
        # Template voxels will have origin at 0,0,0
        # It is easier to scale the nodes from the image affine
        # Then to rescale the ax.voxels function
        # So if affine is not None, nodes get scaled in relation to origin and voxelsize, 
        if fi == 0:
            nodes = _scale_nodes(nodes, affine)
        if edges is not None: 
            _plot_edges(ax, nodes, edges, edgewidth=edgewidth, edgecolor=edgecolor)
        if nodes is not None: 
            _plot_nodes(ax, nodes, nodesize=nodesize, nodecolor=nodecolor)
        if arrowaxis is not None:
            _add_axis_arrows(ax, dims=arrowaxis, length=arrowlength, origin=arroworigin)

        ax.set_box_aspect([1,1,1]) # IMPORTANT - this is the new, key line
        _set_axes_equal(ax) # IMPORTANT - this is also required
        ax.axis('off')
        ax.view_init(azim=azim[fi], elev=elev[fi])
        ax_out.append(ax)
        fig.tight_layout()
    return ax_out
