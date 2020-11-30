
# ax.set_proj_type('ortho') # OPTIONAL - default is perspective (shown in image above)
def _add_axis_arrows(ax, dims=['LR', 'AP'], length=5, origin=[5, 5, 5]):
    """
    dims: list or string
        LR, AP, DV, 'all'
    """
    if dims == 'all':
        dims = ['LR', 'AP', 'DV']
    if isinstance(dims, str):
        dims = [dims]

    arrows_dx = []
    arrows_dy = []
    arrows_dz = []
    # Half the arrow size
    l = length/2
    # Go through each dimension and derive arrow coordinates
    if 'LR' in dims:
        arrows_dx += [-l, l]
        arrows_dy += [0, 0]
        arrows_dz += [0, 0]
        ax.text(origin[0] - l - 1, origin[1], origin[2], 'L', color='gray')
        ax.text(origin[0] + l + 1, origin[1], origin[2], 'R', color='gray')
    if 'AP' in dims:
        arrows_dx += [0, 0]
        arrows_dy += [-l, l]
        arrows_dz += [0, 0]
        ax.text(origin[0], origin[1] - l - 1, origin[2], 'P', color='gray')
        ax.text(origin[0], origin[1] + l + 1, origin[2], 'A', color='gray')
    if 'DV' in dims:
        arrows_dx += [0, 0]
        arrows_dy += [0, 0]
        arrows_dz += [-l, l]
        ax.text(origin[0], origin[1], origin[2] - l - 1, 'V', color='gray')
        ax.text(origin[0], origin[1], origin[2] + l + 1, 'D', color='gray')

    # Arrow origins
    arrows_x = [origin[0]] * (len(dims) * 2)
    arrows_y = [origin[1]] * (len(dims) * 2)
    arrows_z = [origin[2]] * (len(dims) * 2)

    ax.quiver(arrows_x, arrows_y, arrows_z, arrows_dx, arrows_dy, arrows_dz, color='gray')
