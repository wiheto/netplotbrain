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

fig  = plt.figure()

# Surface style 
ax = fig.add_subplot(141, projection='3d')
netplotbrain.plot(template='MNI152NLin6Asym',
                  templatestyle='surface',
                  view='A',
                  arrowaxis=None,
                  subtitles='surface',
                  fig=fig, ax=ax)

# Filled style 
ax = fig.add_subplot(142, projection='3d')
netplotbrain.plot(template='MNI152NLin6Asym',
                  templatestyle='filled',
                  view='A',
                  arrowaxis=None,
                  subtitles='filled',
                  fig=fig, ax=ax)

# Cloudy style 
ax = fig.add_subplot(143, projection='3d')
netplotbrain.plot(template='MNI152NLin6Asym',
                  templatestyle='cloudy',
                  view='A',
                  arrowaxis=None,
                  subtitles='cloudy',
                  fig=fig, ax=ax)

# Glass style 
ax = fig.add_subplot(144, projection='3d')
netplotbrain.plot(template='MNI152NLin6Asym',
                  templatestyle='glass',
                  view='A',
                  arrowaxis=None,
                  subtitles='glass',
                  fig=fig, ax=ax)






