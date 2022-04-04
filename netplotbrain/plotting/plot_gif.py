import io
from PIL import Image


def _plot_gif(fig, ax, gifduration, savename=None, gif_loop=0):

    """
    Create a GIF from plot

    Requires the function 'plot' to contain the paramater 'frames' (two or more frames needed)
    Takes return values from the function 'plot'

    Parameters
    ---------------------

    ax : list of subplot axes

    fig : matplotlib figure

    gifduration: each frame in ms, int (600 is suggested)

    gif_loop: number of loops, int
    If 0, it becomes an infinite loop

    savename: str (default 'netplotbrain.gif')
    Name of the saved GIF

    """

    #Ensure that savename ends in gif
    if savename is None:
        raise ValueError('savename must be specified to save gif')
    # Add give to end of the
    if savename.endswith('.gif') is False:
        savename += '.gif'

    #saving matplotlib figures (frame images) to buffer and opening in PIL Image objects
    images = []

    for i, current_ax in enumerate(ax):
        extent = current_ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        buf = io.BytesIO()
        fig.savefig(buf, bbox_inches=extent, format='PNG', dpi=300)
        buf.seek(i)
        img = Image.open(buf).convert('RGBA')
        images.append(img)

    images[0].save(savename,
                   save_all=True, append_images=images[1:], optimize=False, duration=gifduration, loop=gif_loop)
