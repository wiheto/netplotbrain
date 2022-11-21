#  
# # Different template styles
#
# [Open interactive notebook in Binder](https://mybinder.org/v2/gh/wiheto/netplotbrain/main?filepath=docs/gallery/template_styles.ipynb)
#
# There are currently four different template style options to choose from: suface, filled, cloudy, glass. 
# You just need to change the specification in the template_style argument.

# +
# Import packages
import netplotbrain
import matplotlib.pyplot as plt

netplotbrain.plot(template='MNI152NLin6Asym',
                  template_style=['surface', 'filled', 'cloudy', 'glass'],
                  view='A',
                  arrowaxis=None,
                  subtitles=['surface', 'filled', 'cloudy', 'glass'])
