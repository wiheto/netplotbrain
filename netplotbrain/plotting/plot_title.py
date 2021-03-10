

def _add_subplot_title(ax, azim, elev, title='auto', hemisphere='both', titlefont='Sawasdee', titlefontsize='medium', titleloc='center', titleweight='regular', titlecolor='gray'):

    if title == 'auto':
        viewcoord = (azim, elev)
        title = ''
        if viewcoord == (180, 10):
            title = 'View: Left'
        elif viewcoord == (0, 10):
            title = 'View: Right'
        elif viewcoord == (90, 10):
            title = 'View: Anterior'
        elif viewcoord == (-90, 10):
            title = 'View: Posterior'
        elif viewcoord == (-90, 90):
            title = 'View: Superior'
        elif viewcoord == (90, 90):
            title = 'View: Inferior'
        # Add hemisphere
        if hemisphere == 'L' or hemisphere == 'left':
            title += ' (left hemisphere)'
        elif hemisphere == 'R' or hemisphere == 'right':
            title += ' (right hemisphere)'

    ax.set_title(title, fontname=titlefont,
                     fontweight=titleweight, color=titlecolor,
                     fontsize=titlefontsize,
                     loc=titleloc)

