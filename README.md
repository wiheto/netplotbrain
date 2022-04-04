# netplotbrain: visualizing networks in 3D on a brain

[![CircleCI](https://circleci.com/gh/wiheto/netplotbrain.svg?style=shield)](https://app.circleci.com/pipelines/github/wiheto/netplotbrain)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d2c620d4be8047989e7b91ac3bbbba97)](https://www.codacy.com/gh/wiheto/netplotbrain/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wiheto/netplotbrain&amp;utm_campaign=Badge_Grade)
[![DOI](https://zenodo.org/badge/317297000.svg)](https://zenodo.org/badge/latestdoi/317297000)
[![Coverage Status](https://coveralls.io/repos/github/wiheto/netplotbrain/badge.svg?branch=main)](https://coveralls.io/github/wiheto/netplotbrain?branch=main)

Painlessly plot networks on a brain in python. The package is still in early development and better documentation/tutorials/examples are in the works.

![](https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/figures/showcase.png)

## Features

1. Easy to specify properties: integration with pandas entails node and edge size/colour can easily be specified.
2. Flexibility: multiple node and template styles. Easily create multiple angles to view the figure.
3. [TemplateFlow](https://www.templateflow.org) integration to download any template or atlas.

## Installation

`pip install git+https://www.github.com/wiheto/netplotbrain`

Note: We will release on pypi soon.

## How it works

There are three components: (1) the nodes, (2) the edges, (3) the template

Each component functions independently.
You do not need to have all of them specified.

## Nodes

There are two ways to specify nodes.

1. Nodes: a pandas dataframe of coordinates

2. Nodeimg: a 3D nifti image where each node has a different value.
Alternatively, nodeimg can be dictionary to grab an atlas from templateflow.

### Nodes (Dataframe)

The Pandas dataframe should have (at least) the columns 'x', 'y', and 'z'.
These columns should be coordinates in the space of the template (e.g. MNI).
It will look something like this.

| x       | y     | z     |
| :-------------:  | :----------: | :-----------: |
|  40     | 50    | 20    |
| -10     | 40    | 30    |

Other columns can be used to style the node's colour and size.
These just become other columns in the dataframe.

| x       | y     | z     | communities | degree_centrality |
| :-------------:  | :----------: | :-----------: | :----------: | :-----------: |
|  40     | 50    | 20    | 1    | 0.8
| -10     | 40    | 30    | 1    | 0.4

With this information, you can easily specify colour and size arguments by specifying the column name:

```netplotbrain.plot(..., nodecolor='communities')```

These additional values to specify size and color can be given as a dataframe even
if you specify your nodes with a nifti image.

### Nodeimg (Nifti image)

You can also input a 3D nifti image where each node is a unique value.

### Nodeimg (Templateflow atlas)

If you specify the key/value pairs of an atlas on templateflow in a dictionary,
the atlas will be automatically downloaded.
For example, the following will get the Schaefer2018 atlas.

```python
nodeimg={'template': 'MNI152NLin2009cAsym',
         'atlas': 'Schaefer2018',
         'desc': '400Parcels7Networks',
         'resolution': 1}
```

See templateflow.org for more atlases.

If the template argument is specified in `netplotbrain.plot`,
then the template argument does not need to be included in the dictionary.

## Edges (dataframe)

Edges as a numpy array (adj matrix) or as a pandas dataframe (edgelist) with the default columns 'i', 'j', and 'weight' (optional). An example:

| j       | j     | weight     |
| :-------------:  | :----------: | :-----------: |
|  0     | 1    | 0.8    |
|  1     | 2    | 0.5    |

`i` and `j` reference the indicies in . You can use the argument `edgecol` to specify different column names.

If numpy array, then the array should be a N x N array (where N is number of nodes).

## Template (nifti or string)

For the template you can supply any nifti file.

You can also provide the template name for any template on templateflow.org.
The T1w brain mask will then automatically downloaded (if not already present on your computer) and used as the background.

Netplotbrain can render slightly different templates

### Template Styles

There are currently three background styles: "surface", "filled" and "cloudy".

The surface quickly renders a surface from the voxels. Additional arguments can be provided in order to the resolution of the surface.

The filled style plots the template's brain mask as voxels. This can be slightly RAM consuming.

The cloudy style tries to identify the outline of the mask and plots points along the edges. The cloudy style is quick, but the edge detection is run relative to the specified initial view of the plot.

For templates, you can change the voxelsize of the template. Larger voxels means the plot will be generated quicker.

## Views

The view is the angle which the brain is viewed from in the plot.
You can specify it as a string:

- Left 'L',
- Right 'R',
- Anterior 'A',
- Posterior 'P'
- Superior 'S'
- Inferior 'I'

Sequences of views are possible.
So, setting view = 'LSR' will generate 3 subplots with left, superior, and right views

You can also specify the specific rotation (tuple): (xy-rotate, xz-rotate) in degrees. The R view is (0, 0)

### Rotated sequences with frames

You can also generate a sequence of rotated images.

If the view is two letters, (e.g. `'LR'`), then a sequence will be generated from the L-view to R-view.

The parameter `frames` will control how many images are generated.
Images will then be displayed along a single row.

If you specify a list (e.g. `['LR', 'AP']`) then two different rows will be generated.
The first from left to right. The second from anterior to posterior.

## Minimal examples

### Import necessary packages and load example data

```python

import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt

# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

```

### Plot single view

```python
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view='R',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges)
plt.show()
```
![](./examples/figures/singleview.png)

### Specify column names to specify size

```python
fig = plt.figure()
ax_m2 = fig.add_subplot(121, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  fig = fig,
                  ax = ax_m2,
                  view='A',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  nodecolor='red',
                  edges=edges)

ax_m2 = fig.add_subplot(122, projection='3d')
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  fig = fig,
                  ax = ax_m2,
                  view='A',
                  nodes=nodes,
                  nodesize='centrality_measure2',
                  nodecolor='blue',
                  edges=edges)
plt.show()
```
![](./examples/figures/measures.png)

### Plot multiple rows

```python
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  view=['LSR', 'AIP'],
                  frames=2)
plt.show()
```
![](./examples/figures/rows1.png)

### Plot atlas (as nodes) from templateflow

```python
netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                            'desc': '400Parcels7Networks',
                            'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['LSR'],
                  nodetype='circles')
plt.show()
```
![](./examples/figures/atlas_circles.png)

### plot atlas (as parcels) from templateflow

```python
netplotbrain.plot(nodeimg={'atlas': 'Schaefer2018',
                            'desc': '400Parcels7Networks',
                            'resolution': 1},
                  template='MNI152NLin2009cAsym',
                  templatestyle=None,
                  view=['LSR'],
                  nodetype='parcels',
                  nodealpha=0.5,
                  nodecolor='Set3')
plt.show()
```
![](./examples/figures/atlas_parcels.png)

### Plot individual hemispheres

```python
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view=['SSS'],
                  hemisphere=['L', 'R', ''],
                  nodes=nodesdf,
                  nodesize='centrality_measure1',
                  edges=edges)
```
![](./examples/figures/hemi.png)

### Plot different templates

```python
# rat template
# Setting templatevoxsize to 0.2 will make it slightly quicker
# Due to the voxel size being smaller, the nodes are currently smaller
# So scaling the nodes is useful.
nodes_whs = nodes.copy()
nodes_whs['x'] = nodes_whs['x'] / 8
nodes_whs['y'] = nodes_whs['y'] / 8
nodes_whs['z'] = nodes_whs['z'] / 8
netplotbrain.plot(template='WHS',
         templatestyle='surface',
         title='Multiple templates possible',
         view='LSR',
         nodes=nodes_whs,
         nodesize='centrality_measure1',
         edges=edges,
         nodecolorby='community',
         nodescale=80,
         templatevoxsize=0.2)

plt.show()
```
![](./examples/figures/template_whs.png)

```python
# infant template
nodes_inf = nodes.copy()
nodes_inf['x'] = nodes_inf['x'] / 1.25
nodes_inf['y'] = nodes_inf['y'] / 1.25
nodes_inf['z'] = nodes_inf['z'] / 1.25
netplotbrain.plot(template='MNIInfant',
         templatestyle='surface',
         title='Infant template',
         view='LSR',
         nodes=nodes_inf,
         nodesize='centrality_measure1',
         nodecolorby='community',
         nodescale=80,
         edges=edges)

plt.show()
```
![](./examples/figures/template_inf.png)

### Plotting a rotating GIF

```python
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='surface',
                  view='AP',
                  frames=10,
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  gif=True,
                  savename='./examples/figures/gif1')
```
![](./examples/figures/gif1.gif)


### Plot different styles

```python
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='filled',
                  view='SPR',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges)
plt.show()
```
![](./examples/figures/styles1.png)

```python
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  templatestyle='cloudy',
                  view='SPR',
                  nodes=nodes,
                  nodesize='centrality_measure1',
                  edges=edges,
                  templatevoxsize=2)
plt.show()
```
![](./examples/figures/styles2.png)

## Get involved

We hope to develop this package.
Please feel free to get in touch about what feature you want/would like to implement/would like to contribute to.

## Citation

If using netplotbrain in an academic article, please cite the package and the libraries it relies on.

Suggestion of text in methods section:

>### Methods
>
>Network plots were generated using netplotbrain (Thompson & Fanton 2021), which utilizes templateflow (Ciric et al 2021), matplotlib (Hunter 2007), pandas (McKinney 2011), numpy (Harris et al 2020), scipy (Virtanen et al 2020), nibabel (Brett et al 2020), and scikit-image (van der Walt et al 2014).
>
>### References
>
>Brett, Matthew, Markiewicz, Christopher J., Hanke, Michael, Côté, Marc-Alexandre, Cipollini, Ben, McCarthy, Paul, et al (2020, November 28). nipy/nibabel: 3.2.1 (Version 3.2.1). Zenodo. http://doi.org/10.5281/zenodo.4295521
>
>Ciric, R., Lorenz, R., Thompson, W. H., Goncalves, M., MacNicol, E., Markiewicz, C., ... & Esteban, O. (2021). TemplateFlow: a community archive of imaging templates and atlases for improved consistency in neuroimaging. bioRxiv.
>
>Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., ... & Oliphant, T. E. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.
>
>Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. IEEE Annals of the History of Computing, 9(03), 90-95.
>
>McKinney, W. (2011). pandas: a foundational Python library for data analysis and statistics. Python for High Performance and Scientific Computing, 14(9), 1-9.
>
>Thompson WH, & Fanton S. (2021, 10 March). wiheto/netplotbrain:. Zenodo. doi :10.5281/zenodo.4593837
>
>Van der Walt, S., Schönberger, J. L., Nunez-Iglesias, J., Boulogne, F., Warner, J. D., Yager, N., ... & Yu, T. (2014). scikit-image: image processing in Python. PeerJ, 2, e453.
>
>Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., ... & van Mulbregt, P. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature methods, 17(3), 261-272.
