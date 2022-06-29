
def _get_presetviews(view):
    """
    If view is one of the following preset strings:


    preset-3 - plots a 1x3 figure with SsLR views

        r1, c1, left view, both hemispheres
        r1, c2, right view, both hemisphere
        r1, c3, left view, both hemispheres 

    preset-4LR - plots a 2x2 figure of each hemisphere

        r1, c1, Left view, left hemisphere
        r1, c2, right view, right hemisphere
        r2, c1, right view, left hemisphere 
        r2, c2, left view, right hemisphere 


    preset-4spring - plots a 2x2 figure with SsLR views

        r1, c1, superior view, both hemispheres
        r1, c2, spring layout view
        r2, c1, left view, both hemispheres 
        r2, c2, right view, both hemispheres

    preset-9 - plots all default views in a 3x3 grid

        r1, c1, left view, left hemispheres
        r1, c2, right view, both hemisphere
        r1, c3, left view, right hemispheres
        r2, c1, right view, left hemispheres
        r2, c2, inferior view, both hemisphere
        r2, c3, left view, right hemispheres 
        r3, c1, anterior view, both hemispheres
        r3, c2, spring layout
        r3, c3, posterior view, both hemispheres 

    
    """

    if view == 'preset-4' or view == 'preset-4LR':
        view = ['LR', 'RL']
        hemisphere = ['LR', 'LR']

    elif view == 'preset-4s' or view == 'preset-4spring':
        view = ['Ss', 'LR']
        hemisphere = 'both'

    elif view == 'preset-3':
        view = ['LRS']
        hemisphere = 'both'

    elif view == 'preset-9':
        view = ['LSR', 'RIL', 'AsP']
        hemisphere = ['LBR', 'LBR', 'BBB']

    elif view == 'preset-6':
        view = ['LSR', 'RAL']
        hemisphere = ['LBR', 'LBR']

    elif view == 'preset-6s' or view == 'preset-6spring':
        view = ['LSR', 'RsL']
        hemisphere = ['LBR', 'LBR']

    else: 
        raise ValueError('Unknown preset value.')


    return view, hemisphere