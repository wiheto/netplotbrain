<a name="netplotbrain"></a>
# netplotbrain

<a name="netplotbrain.plot"></a>
# netplotbrain.plot

<a name="netplotbrain.plot.plot"></a>
#### plot

```python
plot(nodes=None, fig=None, ax=None, view='L', frames=1, edges=None, template=None, templatestyle='filled', templatealpha=0.2, templatevoxsize=None, templatecolor='lightgray', surface_resolution=2, templateedgethreshold=0.7, arrowaxis='auto', arrowlength=10, arroworigin=None, edgecolor='k', nodesize=1, nodescale=5, nodecolor='salmon', nodetype='spheres', nodecolorby=None, nodecmap='Dark2', edgescale=1, edgeweights=True, nodecols=['x', 'y', 'z'], nodeimg=None, nodealpha=1, hemisphere='both', title='auto', highlightnodes=None, edgealpha=1, highlightlevel=0.85, edgehighlightbehaviour='both')
```

Plot a network on a brain

Parameters
---------------------

ax : matplotlib ax with 3D projection
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
bnv.plot(ax, ...)
view : string, list, or tuple
if string: alternatives are 'A' (anterior), 'P' (posteiror), 'L' (left), 'R' (right), 'I' (inferior), 'S' (superior)
or any combination of these (e.g 'LR', 'AP')
The string can contain multiple combinations (e.g. LSR)
if list: multiple strings (as above) which will create new rows of subplots.
if tuple: (azim, elev) where azim rotates along xy, and elev rotates along xz.
If LR or AP view combinations only, you can specify i.e. 'AP-' to rotate in the oposite direction
nodes : dataframe, string
The dataframe must include x, y, z columns that correspond to coordinates of nodes (see nodecols to change this).
Can include additional infomation for node size and color.
If string, can load a tsv file (tab seperator), assumes index column is the 0th column.
edges : dataframe, numpy array, or string
If dataframe, must include i, j columns (and weight, for weighted).
i and j specify indicies in nodes.
See edgecols if you want to change the default column names.
if numpy array, square adjacecny array.
If string, can load a tsv file (tab seperator), assumes index column is the 0th column.
template : str or nibabel nifti
Path to nifti image, or templateflow template name (see templateflow.org) in order to automatically download T1 template.
templatestyle : str
can be 'surface': (a surface is rendered from the template),
'filled': (a single transparant color)
'cloudy': cloudy (cloudy scatter edges outline the figure)
surface_resolution : int
If templatestyle=='surface' controls the size of the triangles used in the surface reconstruction (default: 2).
templatecolor : str
If templatestyle=='surface' or 'filled', the color of template voxels
templateedgedetection : float
If templatestyle=='cloudy', can tweak the edges detection threshold.
templatealpha : float
Opacity of template voxels.
templatevoxelsize : int
Resize voxels this size. Larger voxels = quicker. Default = 2
arrowaxis : list or str
Adds axis arrows onto plot. Alternatives are: LR, AP, SI, 'all'
arrowlength : int, float
Length of arrow
arroworigin : list
x,y,z coordinates of arrowaxis. Note 0,0,0 is bottom left.
edgecolor : matplotlib coloring
Can be string (default 'black') or list of 3D/4D colors for each edge.
edgewidth : int, float
Specify width of edges. If auto, will plot the value in edge array (if array) or the weight column (if in pandas dataframe), otherwise 2.
edgeweights : string
String that specifies column in edge dataframe that contains weights.
If numpy array is edge input, can be True (default) to specify edge weights.
edgealpha : float
Transparency of edges.
nodesize : str, int, float
If string, can plot a column
nodecolorby : str
Column in dataframe that should get different colors (cannot be set with nodecolor)
nodecmap : str
Matplotlib colormap for node coloring with nodecolorby.
nodecolor : matplotlib coloring
Can be string (default 'black') or list of 3D/4D colors for each edge.
nodetype : str
Can be 'spheres', 'circles', or (if nodeimg is specified) 'parcels'.
nodeimg : str or nii
String to filename or nibabel object that contains nodes as int.
nodealpha : float
Specify the transparency of the nodes
frames : int
If specifying 2 views (e.g. LR or AP) and would like to rotates a between them.
This value will indicate the number of rotations to get from L to R.
For any other view specification, (e.g. specifying string such as 'LSR')
then this value is not needed.
hemisphere: string or list
If string, can be left or right to specify single hemisphere to include.
If list, should match the size of views and contain strings to specify hemisphere.
Can be abbreviated to L, R and (empty string possible if both hemisphere plotted).
Between hemispehre edges are deleted.
nodecols : list
Node column names in node dataframe. Default is x, y, z (specifying coordinates)
edgecols : list
Edge columns names in edge dataframe. Default is i and j (specifying nodes).
highlightnodes : int, list, dict
List or int point out which nodes you want to be highlighted.
If dict, should be a single column-value pair.
Example: highlight all nodes of that, in the node dataframe, have a community
value of 1, the input will be {'community': 1}.
highlightlevel : float
Intensity of the highlighting (opposite of alpha).
Value between 0 and 1, if 1, non-highlighted nodes are fully transparent.
If 0, non-highlighted nodes are same alpha level as highlighted nodes.
Default 0.85.
edgehighlightbehaviour : str
Alternatives "both" or "any" or None.
Governs edge dimming when highlightnodes is on
If both, then highlights only edges between highlighted nodes.
If any, then only edges connecting any of the nodes are highlighted.

<a name="netplotbrain.plotting"></a>
# netplotbrain.plotting

<a name="netplotbrain.plotting.plot_nodes"></a>
# netplotbrain.plotting.plot\_nodes

<a name="netplotbrain.plotting.process_input"></a>
# netplotbrain.plotting.process\_input

<a name="netplotbrain.plotting.process_input.get_frame_input"></a>
#### get\_frame\_input

```python
get_frame_input(inputvar, axind, ri, fi)
```

Gets subplot varible depnding on whether the
input is a string, array or 2d array.

<a name="netplotbrain.plotting.plot_spheres"></a>
# netplotbrain.plotting.plot\_spheres

<a name="netplotbrain.plotting.plot_title"></a>
# netplotbrain.plotting.plot\_title

<a name="netplotbrain.plotting.plot_edges"></a>
# netplotbrain.plotting.plot\_edges

<a name="netplotbrain.plotting.plot_templates"></a>
# netplotbrain.plotting.plot\_templates

<a name="netplotbrain.plotting.plot_parcels"></a>
# netplotbrain.plotting.plot\_parcels

<a name="netplotbrain.plotting.plot_dimarrows"></a>
# netplotbrain.plotting.plot\_dimarrows

<a name="netplotbrain.utils"></a>
# netplotbrain.utils

<a name="netplotbrain.utils.coloring"></a>
# netplotbrain.utils.coloring

<a name="netplotbrain.utils.plot_utils"></a>
# netplotbrain.utils.plot\_utils

<a name="netplotbrain.__version"></a>
# netplotbrain.\_\_version

<a name="netplotbrain.templatesettings"></a>
# netplotbrain.templatesettings

<a name="netplotbrain.templatesettings.surface_detection"></a>
# netplotbrain.templatesettings.surface\_detection

