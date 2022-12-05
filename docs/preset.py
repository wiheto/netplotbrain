# %% [markdown]
""" 
# Preset viewing angles 

This notebook shows the preset combinations that exist in netplotbrain that can be specified by setting the keyword argument `view` to the following  
"""

# %%
# import necessary packages and load example data
import pandas as pd
import netplotbrain
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

# %% [markdown]
""" 
# view='preset-3'
"""
# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='preset-3',
                  nodes=nodes,
                  edges=edges)

# %% [markdown]
""" 
# view='preset-4'
"""
# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='preset-4',
                  nodes=nodes,
                  edges=edges)

# %% [markdown]
""" 
# view='preset-4spring' (alt: preset-4s)
"""
# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='preset-4spring',
                  nodes=nodes,
                  edges=edges)

# %% [markdown]
""" 
# view='preset-9'
"""
# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='preset-9',
                  nodes=nodes,
                  edges=edges)

# %% [markdown]
""" 
# view='preset-6'
"""
# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='preset-6',
                  nodes=nodes,
                  edges=edges)

# %% [markdown]
""" 
# view='preset-6spring' (alt: preset-6s)
"""
# %%
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='preset-6spring',
                  nodes=nodes,
                  edges=edges)

