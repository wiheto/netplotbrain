import numpy as np
import matplotlib.pyplot as plt

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
    """
    direction = '+'
    if views[-1] == '-' or views[-1] == '+':
        direction = views[-1]
        views = views[:-1]

    # Order = LRAPDV
    fromview = views[0]
    toview = views[1] if len(views) == 2 else None
    view_defaults = {'L': (180, 10), 'R': (0, 10),
                     'A': (90, 10), 'P': (-90, 10),
                     'S': (-90, 90), 'I': (90, 90)}
    # Set auto arrows for axis depedning on starting view
    if fromview in ['L', 'R']:
        autoarrowaxis = 'AP'
    elif fromview in ['A', 'P']:
        autoarrowaxis = 'LR'
    elif fromview in ['S', 'I']:
        autoarrowaxis = ['LR', 'AP']
    # If multiple letters are specified or one view specified
    # Then just get default
    if len(views) == frames or len(views) != 2:
        vx = []
        vy = []
        for view in views:
            vxtmp, vytmp = view_defaults[view]
            vx.append(vxtmp)
            vy.append(vytmp)
    # Otherwise rotate figure based on frames iput
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
    if arrowaxis == 'auto':
        arrowaxis = autoarrowaxis
    return vx, vy, arrowaxis
