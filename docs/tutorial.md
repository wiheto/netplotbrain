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

The other columns in the dataframe can refer to node related properties (e.g. size and colour). In such cases the dataframe may begin something like this: 

These just become other columns in the dataframe (called node_df).

| x       | y     | z     | communities | degree_centrality |
| :-------------:  | :----------: | :-----------: | :----------: | :-----------: |
|  40     | 50    | 20    | 1    | 0.8
| -10     | 40    | 30    | 1    | 0.4

Then the columns `nodecolor=communities`and `nodesize=degree_centrality` be specified and each node will automatically be coloured or scaled by the specified column. For example: 

```python
netplotbrain.plot(
    nodes=nodes_df,
    nodesize='degree_centrality'
    nodecolor='communities')
```
 
Will just plot the nodes, with each node having the size of the degree_centrality column and a colour of the communities column. 
  
#### A pandas dataframe (Argument: nodes) 

Instead of having coordinates of nodes, you can specify images instead.

If specifying `nodeimg` for the coordinates of the nodes, then you need can still apply property arguments by supplying a dataframe to the `nodes`. 

## Section 2: customization 

In this section, we expand upon the basics knowledge and start to customize the plots. 