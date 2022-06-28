

def _add_subplot_title(ax, azim=None, elev=None, subtitle='auto', hemisphere='both', viewtype='b', **kwargs):
    subtitlefont = kwargs.get('font')
    subtitlecolor = kwargs.get('fontcolor')
    subtitlefontsize = kwargs.get('subtitlefontsize')
    subtitleloc = kwargs.get('subtitleloc')
    subtitleweight = kwargs.get('subtitleweight')
    if subtitle == 'auto':
        viewcoord = (azim, elev)
        subtitle = ''
        if viewcoord == (180, 10):
            subtitle = 'Left'
        elif viewcoord == (0, 10):
            subtitle = 'Right'
        elif viewcoord == (90, 10):
            subtitle = 'Anterior'
        elif viewcoord == (-90, 10):
            subtitle = 'Posterior'
        elif viewcoord == (-90, 90) and viewtype == 'b':
            subtitle = 'Superior'
        elif viewcoord == (90, 90):
            subtitle = 'Inferior'
        # Add hemisphere
        if hemisphere == 'L' or hemisphere == 'left':
            subtitle += ' (left hemisphere)'
        elif hemisphere == 'R' or hemisphere == 'right':
            subtitle += ' (right hemisphere)'

    ax.set_title(subtitle, fontname=subtitlefont,
                     fontweight=subtitleweight, color=subtitlecolor,
                     fontsize=subtitlefontsize,
                     loc=subtitleloc)
    


def _add_title(fig, **kwargs):
    title = kwargs.get('title')
    titlefont = kwargs.get('font')
    titlecolor = kwargs.get('fontcolor')
    titlefontsize = kwargs.get('titlefontsize')
    titleweight = kwargs.get('titleweight')
        
    fig.suptitle(title, fontname=titlefont,
                     fontweight=titleweight, 
                     color=titlecolor,
                     fontsize=titlefontsize)
    