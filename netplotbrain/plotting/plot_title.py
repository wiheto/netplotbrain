

def _add_subplot_title(ax, azim=None, elev=None, title='auto', hemisphere='both', **kwargs):
    titlefont = kwargs.get('font')
    titlecolor = kwargs.get('fontcolor')
    titlefontsize = kwargs.get('titlefontsize')
    titleloc = kwargs.get('titleloc')
    titleweight = kwargs.get('titleweight')
    if title == 'auto':
        viewcoord = (azim, elev)
        title = ''
        if viewcoord == (180, 10):
            title = 'Left'
        elif viewcoord == (0, 10):
            title = 'Right'
        elif viewcoord == (90, 10):
            title = 'Anterior'
        elif viewcoord == (-90, 10):
            title = 'Posterior'
        elif viewcoord == (-90, 90):
            title = 'Superior'
        elif viewcoord == (90, 90):
            title = 'Inferior'
        # Add hemisphere
        if hemisphere == 'L' or hemisphere == 'left':
            title += ' (left hemisphere)'
        elif hemisphere == 'R' or hemisphere == 'right':
            title += ' (right hemisphere)'

    ax.set_title(title, fontname=titlefont,
                     fontweight=titleweight, color=titlecolor,
                     fontsize=titlefontsize,
                     loc=titleloc)

