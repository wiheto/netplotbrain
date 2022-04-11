# Tutorial

In this section there are files on different components of netplotbrain.

The tutorial is split into two section. 

## Section 1: the basics

There are three components: 

1. the nodes, 
2. the edges, 
3. the template

Each component and their properties are  plotted independently of each other.

### 1.1 Specifying Nodes

There are two ways you can specify the coordinates of the nodes. 

#### A pandas dataframe (Argument: nodes) 

To plot the nodes, the pandas dataframe must contain three columns that refer to the 3D coordinates of each node. By default, these columns are called `x`, `y`, `z` by they can be manually specified by called the `colnames` keyword argument. 

Thus, the dataframe will begin something like this:

| x       | y     | z     |
| :-------------:  | :----------: | :-----------: |
|  40     | 50    | 20    |
| -10     | 40    | 30    |

If we create this dataframe with the two nodes above, we will just plot two circles onto the figure. 

```python
# Import packages
import netplotbrain
import pandas as pd
# Define the nodes
nodes_df = pd.DataFrame({'x': [40, 10, 30, -15, -25], 
                         'y': [50, 40, -10, -20, 20], 
                         'z': [20, 30, -10, -15, 30]})
# Call netplotbrain to plot
netplotbrain.plot(nodes=nodes_df, arrowaxis=None)
```

Here we just see five dots of the same size, but we have nodes in the 3D space. 

The second option `arrowaxis` turns of some default directional arrows which do not look good in this small-scale example without a background template.

The other columns in the dataframe can refer to node related properties (e.g. size and colour). In such cases the dataframe may begin something like this: 

These just become other columns in the dataframe (called node_df).

| x       | y     | z     | communities | degree_centrality |
| :-------------:  | :----------: | :-----------: | :----------: | :-----------: |
|  40     | 50    | 20    | 1    | 0.8
| -10     | 40    | 30    | 1    | 0.4

Then the columns `nodecolor=communities`and `nodesize=degree_centrality` be specified and each node will automatically be coloured or scaled by the specified column. For example: 

```python
# Import packages
import netplotbrain
import pandas as pd
# Define the nodes (5 example nodes)
nodes_df = pd.DataFrame(data={'x': [40, 10, 30, -15, -25], 
                              'y': [50, 40, -10, -20, 20], 
                              'z': [20, 30, -10, -15, 30], 
                              'communities': [1, 1, 1, 2, 2], 
                              'degree_centrality': [1, 1, 0.2, 0.8, 0.4]})
# Call netplotbrain to plot
netplotbrain.plot(
    nodes=nodes_df,
    nodesize='degree_centrality',
    nodecolorby='communities',
    arrowaxis=None,
    nodescale=100)
```
 
Will just plot the nodes, with each node having the size of the degree_centrality column and a colour of the communities column. Here we have also added `nodescale` which just linearly scales all nodes by that factor. We also see that when specifying nodesize and nodecolorby that legends automatically appear.

At the moment we just have some circles floating in 3D space. Let us add some more information about this network.

## Edges

The edges between the nodes can be passed to netplotbrain as either a numpy array (NxN adjacency matrix) or a pandas dataframe (edgelist) with the default columns 'i', 'j', and 'weight' (optional). An example:

| j       | j     | weight     |
| :-------------:  | :----------: | :-----------: |
|  0     | 1    | 0.8    |
|  1     | 2    | 0.5    |

`i` and `j` reference the inidcies of our nodes defined above. You can use the argument `edgecol` to specify different column names.

Let us continue to add to our figure above: 

```python
# Import packages
import netplotbrain
import pandas as pd
# Define the nodes (5 example nodes)
nodes_df = pd.DataFrame(data={'x': [40, 10, 30, -15, -25], 
                              'y': [50, 40, -10, -20, 20], 
                              'z': [20, 30, -10, -15, 30], 
                              'communities': [1, 1, 1, 2, 2], 
                              'degree_centrality': [1, 1, 0.2, 0.8, 0.4]})
# Define the edges 
edges_df = pd.DataFrame(data={'i': [0, 0, 1, 1, 3], 
                              'j': [1, 2, 2, 3, 4]})
# Call netplotbrain to plot
netplotbrain.plot(
    nodes=nodes_df,
    edges=edges_df,
    nodecolorby='communities',
    arrowaxis=None,
    nodescale=150)
```

#### A pandas dataframe (Argument: nodes) 

Instead of having coordinates of nodes, you can specify images instead.

If specifying `nodeimg` for the coordinates of the nodes, then you need can still apply property arguments by supplying a dataframe to the `nodes`. 

## Section 2: customization 

In this section, we expand upon the basics knowledge and start to customize the plots. 