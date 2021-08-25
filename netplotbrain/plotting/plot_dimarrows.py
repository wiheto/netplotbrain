
def _add_axis_arrows(ax, dims=None, origin=None, azim=0, elev=0, **kwargs):
    """
    Plots arrows to show the 3d Axis.

    Parameters
    ---------------------
    ax : matplotlib ax
    dims : list, string
        LR, AP, SI, 'all', None
    origin : list (len of 3)
        Origin of center of arrow axes.
        If none, centers automatically in bottom left.
    azim : int
        azim argument, for origin auto calculation
    elev : int
        elev argument, for origin auto calculation

    kwags
    --------------------
    arrowlength : int, float

    Returns
    -----------------
    Nothing (input axis is updated)

    """
    length = kwargs.get('arrowlength')
    # Set default
    if origin is None:
        xlim = ax.get_xlim3d()
        ylim = ax.get_ylim3d()
        zlim = ax.get_zlim3d()
        origin = [xlim[0] + 15, ylim[0] + 15, zlim[0] + 15]
        if azim > 0:
            origin[1] = ylim[1] - 15
        if azim <= 90 and azim > -90:
            origin[0] = xlim[1] + 15
    # Check the azim to see the orientation of letters
    # S/I needs to be added.
    # Also this could probably be improved upon
    # Based on hard coding
    valign_a = 'center'
    valign_p = 'center'
    valign_l = 'center'
    valign_r = 'center'
    valign_s = 'bottom'
    valign_i = 'top'
    if azim <= 90 and azim > -90:
        halign_l = 'left'
        halign_r = 'right'
        if elev > 45:
            valign_a = 'bottom'
            valign_p = 'top'
            halign_a = 'center'
            halign_p = 'center'
    else:
        halign_l = 'right'
        halign_r = 'left'
        if elev > 45:
            valign_p = 'bottom'
            valign_a = 'top'
            halign_a = 'center'
            halign_p = 'center'
    if azim > 0 and elev <= 45:
        halign_a = 'left'
        halign_p = 'right'
    else:
        halign_a = 'right'
        halign_p = 'left'
    # Check if input is all
    if dims == 'all':
        dims = ['LR', 'AP', 'SI']
    # Check if input is string, make list
    if isinstance(dims, str):
        dims = [dims]
    # Make null lists
    arrows_dx = []
    arrows_dy = []
    arrows_dz = []
    # Half the arrow size forming a radius for an arrow sphere
    radius = length/2
    # Go through each dimension and derive arrow coordinates
    # For each dim, two arrows are plotted going from origin in both directions
    if 'LR' in dims:
        arrows_dx += [-radius, radius]
        arrows_dy += [0, 0]
        arrows_dz += [0, 0]
        ax.text(origin[0] - radius, origin[1], origin[2], 'L', fontsize='xx-small',
                color='gray', horizontalalignment=halign_l, verticalalignment=valign_l)
        ax.text(origin[0] + radius, origin[1], origin[2], 'R', fontsize='xx-small',
                color='gray', horizontalalignment=halign_r, verticalalignment=valign_r)
    if 'AP' in dims:
        arrows_dx += [0, 0]
        arrows_dy += [-radius, radius]
        arrows_dz += [0, 0]
        ax.text(origin[0], origin[1] - radius, origin[2], 'P', fontsize='xx-small',
                color='gray', horizontalalignment=halign_a, verticalalignment=valign_a)
        ax.text(origin[0], origin[1] + radius, origin[2], 'A', fontsize='xx-small',
                color='gray', horizontalalignment=halign_p, verticalalignment=valign_p)
    if 'SI' in dims:
        arrows_dx += [0, 0]
        arrows_dy += [0, 0]
        arrows_dz += [-radius, radius]
        ax.text(origin[0], origin[1], origin[2] - radius, 'I',
                fontsize='xx-small', color='gray', verticalalignment=valign_i)
        ax.text(origin[0], origin[1], origin[2] + radius, 'S',
                fontsize='xx-small', color='gray', verticalalignment=valign_s)
    # Arrow origins
    arrows_x = [origin[0]] * (len(dims) * 2)
    arrows_y = [origin[1]] * (len(dims) * 2)
    arrows_z = [origin[2]] * (len(dims) * 2)
    # Plot arrows with quiver function
    ax.quiver(arrows_x, arrows_y, arrows_z, arrows_dx, arrows_dy,
              arrows_dz, color='gray', linewidth=0.5, arrow_length_ratio=0.5)