# %% [markdown]
""" 
# Different template styles

There are currently four different template style options to choose from: suface, filled, cloudy, glass. 
You just need to change the specification in the templatestyle argument.
"""

# %%
# Import packages
import netplotbrain
import matplotlib.pyplot as plt

netplotbrain.plot(template='MNI152NLin6Asym',
                  templatestyle=['surface', 'filled', 'cloudy', 'glass'],
                  view='A',
                  arrowaxis=None,
                  subtitles=['surface', 'filled', 'cloudy', 'glass'])
