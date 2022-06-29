## API

## Full list of KWARGS

Here is the full list of keyword arguments (KWARGS) that can be used along with `netplotbrain.plot`. Below they are split up in the following sections

1. __Node KWARGS__ - modify the nodes.
2. __Edge KWARGS__ - modify the edges.
3. __Template KWARGS__ - modify the template.
4. __Legend KWARGS__ - modify the figure legend.
5. __Arrow KWARGS__ - modify the direction arrows.
6. __Figure KWARGS__ - configure the figure as a whole.
7. __GIF KWARGS__ - when exporting as a gif.
8. __Text KWARGS__ - text related variables.
9. __Profile KWARGS__ - setting a style profile for all kwargs.

### NODE KWARGS

| Argument | Type | Description |
| --- | --- | --- |
nodes_df | pd.DataFrame | Allows for passing additional edge information if nodes is nifti file or templateflow atlas dictionary. Behaves like nodes when input is dataframe.
nodecmap | str |     Matplotlib colormap for node coloring when nodecolor points to a dataframe. 
nodecolor | matplotlib coloring | Can be string (default 'black') that points to either a matplotlib color or a column in nodes or nodes_df. Alternatively a list of 3D/4D colors for each node. 
nodetype | str | Can be 'spheres', 'circles', or (if nodes is a nifti image) 'parcels'. 
nodealpha | float | Specify the transparency of the nodes
nodecolumnnames | list | Node column names in node dataframe. 'auto' entails the columns are ['x', 'y', 'z'] (specifying coordinates)
nodesizevminvmax | str, list | Scaling alternatives if nodesize is given. Alternatives: 'absolute' (default) 'minmax', or 2-tuple list of [min, max]. If minmax, node sizes are scaled between (0 and 1) * nodescale. If absolute, then the default values are used. Absolute can lead to problems with, for example, negative values.
nodecolorvminvmax | str, list | Scales continuous colormap between certain values. Alternatives: 'minmax' (default), 'absmax', , or 2-tuple list of [min, max]. If minmax, colorbar starts at the smallest value to largest value. If absmax, then colorbar goes from -abs(max(value)) to abs(max(value)), ensuring 0 is in the middle.

### EDGE KWARGS

| Argument | Type | Description |
| --- | --- | --- |
edges_df | pd.DataFrame | Allows for passing additional edge information if edges is np.array. Behaves like edges when input is dataframe.
edgecmap | str |     Matplotlib colormap for node coloring when nodecolor points to a dataframe. |
edgealpha | float | Transparency of edges (default: 1).
edgecolumnames | list | Edge columns names in edge dataframe. Default is i and j (specifying nodes).
edgecolor | matplotlib coloring | Can be string (default 'black') or list of 3D/4D colors for each edge.
edgeweights | str | String that specifies column in edge dataframe that contains weights. If numpy array is edge input, can be True (default) to specify edge weights.
edgehighlightbehaviour | str | Alternatives "both" or "any" or None. Governs edge dimming when highlightnodes is on. If both, then highlights only edges between highlighted nodes. If any, then only edges connecting any of the nodes are highlighted.
edgewidthscale | int, float | Scale the width of all edges by a factor (default: 1).
edgethresholddirection | str | can be "absabove", "above" (or ">"), "below" (or "<") to indicate thresholding behaviour. If absabove, then the thresholding behaviour is np.abs(edges) > edgethreshold. 
edgethreshold | float | Edgeweight value to threshold edges. 
edgecolorvminvmax | str, list |     Scales colormap between certain values. Alternatives: 'minmax' (default), 'absmax', or 2-tuple list of [min, max]. If minmax, colorbar starts at the smallest value to largest value. If absmax, then colorbar goes from -abs(max(value)) to abs(max(value)), ensuring 0 is in the middle.

### TEMPLATE KWARGS

| Argument | Type | Description |
| --- | --- | --- |
tempalte | str, dict or nibabel nifti | The background template. If str: path to nifti image, or templateflow template name (see templateflow.org) in order to automatically download T1 template. If dict, specify keyword - value pairs for templateflow.api.get(). If specifying templateflow string, and there are multiple cohorts (e.g. MNIInfant) add "_cohort-X" to the string. For example, for MNIInfant, cohort 3, write: "MNIInfant_cohort-3".
templatealpha | float | Opacity of template voxels.
templatecolor | str | If templatestyle=='surface' or 'filled', the color of template voxels
templateedgethreshold | float | If templatestyle=='cloudy', can tweak the edges detection threshold. (Default: 0.7)
templatestyle | str | can be 'surface': (a surface is rendered from the template), 'glass': a semi-transparanet brain is generated from the template. 'filled': plot all voxels, 'cloudy': cloudy (cloudy scatter edges outline the figure)
templatevoxelsize | int | Resize voxels this size. Larger voxels = quicker. (Default: 2)
surface_detection | float | The value used to detect the surface boundary (see argument level in marching_cubes). Some default choices are made for various templates
surface_resolution | int | If templatestyle=='surface' controls the size of the triangles used in the surface reconstruction. (Default: 2).
template_glass_compactness | float | Default 0.3. Compactness argument for skimage.segmentation.slic for segementation. Going lower will increase the detail. >1 will break the figure.
temlate_glass_nsegments | int | n_segments argument for skimage.segementations.slic. Approx number of segments. 3 seems to work well. Increase if not enough detail, reduce if too much detail.
template_glass_maxalpha | float | Default is 0.01. To make the smokey effect the alpha is relative to template intensity value This value sets the alpha scalar factor. The value will be the largest possible alpha value, where all other values scale between 0 and template_glass_max_alpha.

### HIGHLIGHTING KWARGS

highlightlevel | float | Intensity of the highlighting (opposite of alpha). Controls both nods and edges together. Value between 0 and 1, if 1, non-highlighted nodes are fully transparent. If 0, non-highlighted nodes are same alpha level as highlighted nodes. Default 0.85.

See also nodehighlight* and edgehighlight* kwargs.

### LEGENDKWARGS

| Argument | Type | Description |
| --- | --- | --- |    
legendtickfontsize | str, int | Matplotlib fontsize for title in figure legends
legendtitlefontsize | str, int | Matplotlib fontsize for ticks in figure legends
nodecolorlegend | Bool | If the colorlegend is plotted or not. Default True.
nodesizelegend | Bool | If the sizelegend is plotted or not. Default True.
nodecolorlegendstyle | str | Alternatives: auto (default), discrete, continuous. If the color legend should show the entire colormap or discrete colors. If auto, plots discrete if less than 8 unique values are detected.
showlegend | bool, list | If size or colour have been set, generates a legend for that property at bottom of figure. If True, plots all the legends that can be plotted. If list, can contain 'nodesize' and 'nodecolor' to plot those in the legend.

### ARROW KWARGS

| Argument | Type | Description |
| --- | --- | --- |
arrowaxis | list or str | Adds axis arrows onto plot. Alternatives are: LR, AP, SI, 'all'
arrowlength | int, float | Length of arrow
arroworigin | list | x,y,z coordinates of arrowaxis. Note 0,0,0 is bottom left.

### FIGURE KWARGS

| Argument | Type | Description |
| --- | --- | --- |
ax | matplotlib 3D ax | fig = plt.figure(). ax = fig.add_subplot(111, projection='3d'). netplotbrain.plot(ax, ...)
fig | matplotlib figure
savename | str | Save path for figure. If string ends with .png or .svg it will one save this figure. if the path ends with anything else, it will save both a .png and .svg figure. Default: None and nothing is saved.
figdpi | int | 300 Default. R   esolution of figure when saving png files.

### HEMISPHERE KWARGS
| Argument | Type | Description |
| --- | --- | --- |
hemisphere | string, list | If string, can be left or right to specify single hemisphere to include. If list, should match the size of views and contain strings to specify hemisphere shown in subplots. Can be abbreviated to "L", "R" and ("both" or empty string possible if both hemisphere plotted). Between hemisphere edges are deleted.

### GIF KWARGS

| Argument | Type | Description |
| --- | --- | --- |
gif | bool | If true, saves views as a gif.
gifduration | int | Gif duration in milliseconds
gifloop | int | How many times to loop figure. 0 (default) entails infinite loop.

### TEXT KWARGS

| Argument | Type | Description |
| --- | --- | --- |
font | str | font for all text in figure.
fontcolor | str, list, tuple | font color for all text in figure
titlefontsize | str | Size of title font (default: medium). See matplotlib "fontsize"
titleloc | str, | Location of title (default: center). See matplotlib "loc"
titleweight | str | Font weight of title (default: regular). See matplotlib "fontweight"

### Other KWARGS

| Argument | Type | Description |
| --- | --- | --- |
seed | int | Pseudorandom integer seed for reproducibility for certain functions (e.g. spring_layout)
profile | str | path or name of file in netplotbrain/profiles/<filename>.json, specifies default kwargs. Default points to netplotbrain/profiles/default.json
