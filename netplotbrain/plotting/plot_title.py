

def _add_subplot_title(ax, azim=None, elev=None, subtitle_frame='auto', hemisphere='both', viewtype='b', **kwargs):
    subtitlefont = kwargs.get('font')
    subtitlecolor = kwargs.get('fontcolor')
    subtitle_fontsize = kwargs.get('subtitle_fontsize')
    subtitle_loc = kwargs.get('subtitle_loc')
    subtitle_weight = kwargs.get('subtitle_weight')
    if subtitle_frame == 'auto':
        viewcoord = (azim, elev)
        subtitle_frame = ''
        if viewcoord == (180, 0):
            subtitle_frame = 'Left'
        elif viewcoord == (0, 0):
            subtitle_frame = 'Right'
        elif viewcoord == (90, 0):
            subtitle_frame = 'Anterior'
        elif viewcoord == (-90, 0):
            subtitle_frame = 'Posterior'
        elif viewcoord == (-90, 90) and viewtype == 'b':
            subtitle_frame = 'Superior'
        elif viewcoord == (90, -90):
            subtitle_frame = 'Inferior'
        # Add hemisphere
        if hemisphere == 'L' or hemisphere == 'left':
            subtitle_frame += ' (left hemisphere)'
        elif hemisphere == 'R' or hemisphere == 'right':
            subtitle_frame += ' (right hemisphere)'

    ax.set_title(subtitle_frame, fontname=subtitlefont,
                     fontweight=subtitle_weight, color=subtitlecolor,
                     fontsize=subtitle_fontsize,
                     loc=subtitle_loc)

def _add_title(fig, **kwargs):
    title = kwargs.get('title')
    titlefont = kwargs.get('font')
    titlecolor = kwargs.get('fontcolor')
    title_fontsize = kwargs.get('title_fontsize')
    title_weight = kwargs.get('title_weight')

    fig.suptitle(title, fontname=titlefont,
                     fontweight=title_weight,
                     color=titlecolor,
                     fontsize=title_fontsize)
