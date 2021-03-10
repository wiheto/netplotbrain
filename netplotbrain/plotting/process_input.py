def get_frame_input(inputvar, axind, ri, fi):
    """Gets subplot varible.
    
    The variable depends on whether the
    input is a string, array or 2d array.
    """
    if isinstance(inputvar, str):
        var_frame = inputvar
    elif isinstance(inputvar[0], str): 
        var_frame = inputvar[axind]
    else: 
        var_frame = inputvar[ri][fi]
    return var_frame