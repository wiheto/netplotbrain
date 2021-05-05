
def _setup_legend(property, legend, legendname, currentlegend=None):
    # If the condition has been specified
    # And if the legend for that property is true
    if isinstance(property, str) and legend == True:
        # If currentlegend is None, initailize 
        if currentlegend is None: 
            currentlegend = []
        currentlegend += [legendname]
    return currentlegend

def _add_size_legend():
    pass

def _add_color_legend():
    pass

