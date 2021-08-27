import io
from PIL import Image


def create_gif(fig, ax, gifname='netplotbrain.gif'):
    """
    Create a GIF from plot

    Requires the function 'plot' to contain the paramater 'frames' (two or more frames needed)
    Takes return values from the function 'plot'

    Parameters
    ---------------------

    ax : list of subplot axes

    fig : matplotlib figure

    gifname: str (default 'netplotbrain.gif')
    Name of the saved GIF

    """

    images = []

    for i, currax in enumerate(ax):
        extent = currax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        buf = io.BytesIO()
        fig.savefig(buf, bbox_inches=extent, format='PNG', dpi=300)
        buf.seek(i)
        img = Image.open(buf).convert('RGBA')
        images.append(img)

    del images[(len(images)-1)//2]

    images[0].save(gifname,
                   save_all=True, append_images=images[1:], optimize=False, duration=600, loop=0)  # duration = each frame in ms
