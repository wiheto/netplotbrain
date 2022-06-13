###################
Full list of KWARGS
###################

NODE KWARGS
--------------
nodecmap : str
    Matplotlib colormap for node coloring with nodecolorby.
nodecolor : matplotlib coloring
    Can be string (default 'black') or list of 3D/4D colors for each edge.
nodetype : str
    Can be 'spheres', 'circles', or (if nodes is nifti) 'parcels'.
nodealpha : float
    Specify the transparency of the nodes
nodecols : list
    Node column names in node dataframe. 'auto' entails the columns are ['x', 'y', 'z'] (specifying coordinates)
nodesizevminvmax : str, list
    Scaling alternatives if nodesize is given.
    Alternatives: 'absolute' (default) 'minmax', or 2-tuple list of [min, max].
    If minmax, node sizes are scaled between (0 and 1) * nodescale.
    If absolute, then the default values are used.
    Absolute can lead to problems with, for example, negative values.
nodecolorvminvmax : str, list
    Scales continuous colormap between certain values. 
    Alternatives: 'minmax' (default), 'absmax', , or 2-tuple list of [min, max].
    If minmax, colorbar starts at the smallest value to largest value.
    If absmax, then colorbar goes from -abs(max(value)) to abs(max(value)), ensuring 0 is in the middle.

EDGE KWARGS
------------

edgecols : list
    Edge columns names in edge dataframe. Default is i and j (specifying nodes).
edgecolor : matplotlib coloring
    Can be string (default 'black') or list of 3D/4D colors for each edge.
edgewidth : int, float
    Specify width of edges. If auto, will plot the value in edge array (if array) or the weight column (if in pandas dataframe), otherwise 2.
edgeweights : string
    String that specifies column in edge dataframe that contains weights.
    If numpy array is edge input, can be True (default) to specify edge weights.
edgealpha : float
    Transparency of edges (default: 1).
edgehighlightbehaviour : str
    Alternatives "both" or "any" or None.
    Governs edge dimming when highlightnodes is on
    If both, then highlights only edges between highlighted nodes.
    If any, then only edges connecting any of the nodes are highlighted.
edgewidthscale : int, float
    Scale the width of all edges by a factor (default: 1)

TEMPLATE KWARGS
-----------------
templatecolor : str
    If templatestyle=='surface' or 'filled', the color of template voxels
templateedgethreshold : float
    If templatestyle=='cloudy', can tweak the edges detection threshold. (Default: 0.7)
templatealpha : float
    Opacity of template voxels.
templatevoxelsize : int
    Resize voxels this size. Larger voxels = quicker. (Default: 2)
surface_detection : float
    The value used to detect the surface boundary (see argument level in marching_cubes).
    Some default choices are made for various templates
surface_resolution : int
    If templatestyle=='surface' controls the size of the triangles used in the surface reconstruction. (Default: 2).

LEGENDKWARGS
---------------------
nodecolorlegend : True
    If the colorlegend is plotted or not.
nodesizelegend : True
nodecolorlegendstyle : str
    Alternatives: auto (default), discrete, continuous
    If the color legend should show the entire colormap or discrete colors.
    If auto, plots discrete if less than 8 unique values are detected.
legendtickfontsize : str, int
    Matplotlib fontsize for title in figure legends
legendtitlefontsize : str, int
    Matplotlib fontsize for ticks in figure legends

ARROW KWARGS
--------------------
arrowaxis : list or str
    Adds axis arrows onto plot. Alternatives are: LR, AP, SI, 'all'
arrowlength : int, float
    Length of arrow
arroworigin : list
    x,y,z coordinates of arrowaxis. Note 0,0,0 is bottom left.

FIGURE KWARGS
-------------------
ax : matplotlib ax with 3D projection
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    netplotbrain.plot(ax, ...)
fig : matplotlib figure
savename : str
    Save path for figure. 
    If string ends with .png or .svg it will one save this figure. 
    if the path ends with anything else, it will save both a .png and .svg figure.
    Default: None and nothing is saved.  
figdpi : int
    Default. resolution of figure when saving png files. 

GIF KWARGS
-------------------------
gif : bool
    If true, saves views as a gif. 
gifduration : int
    Gif duration in milliseconds
gifloop : int
    How many times to loop figure. 0 (default) entails infinite loop. 

TEXT KWARGS
----------------------
font : str
    font for all text in figure.
fontcolor : str, list, tuple
    font color for all text in figure
titlefontsize : str
    Size of title font (default: medium). See matplotlib "fontsize"
titleloc : str,
    Location of title (default: center). See matplotlib "loc"
titleweight : str
    Font weight of title (default: regular). See matplotlib "fontweight"

STYLE KWARGS
--------------------------
profile : str
    path or name of file in netplotbrain/profiles/<filename>.json, specifies default kwargs.
    Default points to netplotbrain/profiles/default.json

