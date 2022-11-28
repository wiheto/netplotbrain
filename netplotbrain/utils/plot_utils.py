import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# equal scaling solution from @AndrewCox from https://stackoverflow.com/a/63625222
# Functions from @Mateen Ulhaq and @karlo
def _set_axes_equal(ax: plt.Axes):
    """
    Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.

    # Credit for code:
    https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to/63625222#63625222
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    # NOTE, this scaling factor (0.3) might needed to be changed
    # Orginally it was 0.5, and should be checked that all templates
    # Fit this. A template specific scaling factor is possible, if problems
    # arise.
    radius = 0.3 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)


def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])


def _get_view(views='L', frames=1, arrowaxis='auto'):
    """
    Gets a or list of azim and elev arguments for viewing of q
    Viewtype is a string of b or s for brain or springlayout view.
    E.g. viewtype=bbbs means 3 brain and one springlayout in the image row.
    """
    direction = '+'
    if views[-1] == '-' or views[-1] == '+':
        direction = views[-1]
        views = views[:-1]

    # Order = LRAPDV
    fromview = views[0]
    toview = views[1] if len(views) == 2 else None
    view_defaults = {'L': (180, 0), 'R': (0, 0),
                     'A': (90, 0), 'P': (-90, 0),
                     'S': (-90, 90), 'I': (90, -90),
                     's': (-90, 90)}
    # Set auto arrows for axis depending on starting view
    autoarrowaxis = None
    if fromview in ['L', 'R']:
        autoarrowaxis = 'AP'
    elif fromview in ['A', 'P']:
        autoarrowaxis = 'LR'
    elif fromview in ['S', 'I']:
        autoarrowaxis = ['LR', 'AP']
    # If multiple letters are specified or one view specified
    # Then just get default
    if len(views) == frames or (len(views) != 2 and views != '360') :
        vx = []
        vy = []
        for view in views:
            vxtmp, vytmp = view_defaults[view]
            vx.append(vxtmp)
            vy.append(vytmp)
    # Otherwise rotate figure based on frames iput
    else:
        if views == '360':
            v1x, v1y = view_defaults['L']
            v2x, v2y = (view_defaults['L'][0]+360,10)
            # add an extra frame because duplicate frame gets deleted later
            frames += 1
        else:
            v1x, v1y = view_defaults[fromview]
            v2x, v2y = view_defaults[toview]
        vx = []
        vy = []
        for n in range(frames):
            if direction == '+':
                vx.append(v1x + n * ((v2x - v1x) / (frames - 1)))
                vy.append(v1y + n * ((v2y - v1y) / (frames - 1)))
            elif direction == '-':
                # This only works when going from LR- and AP-
                vx.append(v1x - n * ((v2x - v1x) / (frames - 1)))
                vy.append(v1y - n * ((v2y - v1y) / (frames - 1)))
        # remove extra frame in 360
        if views == '360':
            vx = vx[:-1]
            vy = vy[:-1]
    if arrowaxis == 'auto':
        arrowaxis = autoarrowaxis
    # Viewtype
    viewtype = 'b' * len(vx)
    if 's' in views:
        # Assumes there will only ever be one springlayout
        ind = views.index('s')
        viewtype = viewtype[:ind] + 's' + viewtype[ind+1:]
    return vx, vy, arrowaxis, viewtype


def _rotate_data_to_viewingangle(data, azim=0, elev=0, rotateback=False):
    """
    Returns rotated data
    """
    if rotateback:
        azim = azim * -1
        elev = elev * -1
    if azim != 0:
        data = rotate(data, -azim, axes=[0, 1], reshape=False, prefilter=False)
    if elev != 0:
        data = rotate(data, -elev, axes=[0, 2], reshape=False, prefilter=False)
    return data


def _node_scale_vminvmax(nodes, node_size, return_labels=False, **kwargs):
    """
    Scales node_size in relation to node_scale, vmin and vmax.

    The parameter node_sizevminvmax dictates the vmin, vmax behaviour.
    """
    vminvmax = kwargs.get('node_sizevminvmax')
    node_scale = kwargs.get('node_scale')
    node_sizevector = nodes[node_size].copy()
    labelformat = None
    if isinstance(vminvmax, list):
        # If outside custom range, set size to zero
        node_sizevector[node_sizevector < vminvmax[0]] = np.nan
        node_sizevector[node_sizevector > vminvmax[1]] = np.nan
        # After removing scale so that vmin and vmax are lowest and highest numbers
        node_sizevector = (
            node_sizevector - vminvmax[0]) / (vminvmax[1] - vminvmax[0]) * (1.05 - 0.05) + 0.05
    elif isinstance(vminvmax, str):
        if vminvmax == 'maxabs':
            node_sizevector = np.abs(node_sizevector)
            # now make sure behaviour is like minmax scaling but labelformat is maxabs
            vminvmax = 'minmax'
            labelformat = 'maxabs'
        if vminvmax == 'minmax':
            # Add small value to ensure smallest value is not 0.1 and 1.1 to ensure min value is still seen
            # TODO this value could be scaled.
            node_sizevector = (node_sizevector - node_sizevector.min()) / \
                (node_sizevector.max() - node_sizevector.min()) * (1.05 - 0.05) + 0.05

    node_sizevector = node_sizevector * node_scale
    if return_labels:
        node_sizelabels = nodes[node_size].copy()
        node_sizelabels[np.isnan(node_sizevector)] = np.nan
        if labelformat == 'maxabs':
            node_sizelabels = np.abs(node_sizelabels)
    # If node_sizevector is nan, make them 0
    node_sizevector[np.isnan(node_sizevector)] = 0
    # If return labels, make output a tuple
    if return_labels:
        node_sizevector = (node_sizevector, node_sizelabels)
    return node_sizevector


def _nrows_in_fig(view, frames):
    """
    Return the number of rows and modify the view and frame input
    """
    # If frames is None, make length of view.
    if frames is None:
        frames = len(view)
    # get the number of views
    if isinstance(view, list):
        nrows = len(view)
    else:
        nrows = 1
        view = [view]
    # remove +- from when checking length of view
    view_frame_checker = str(view[0])
    view_frame_checker = view_frame_checker.replace('+', '').replace('-', '')
    # If specific views are given, calculate value of frames.
    if len(view_frame_checker) > 2 and view_frame_checker != '360':
        frames = len(view_frame_checker)
    return nrows, view, frames
