import pandas as pd

def _networkx_nodes_to_nodesdf(nxgraph, nodecols):
    """
    Takes networkx graph input and returns with the node information in dataframe format for netplotbrian.
    Checks if all node_columnnames (i.e. x, y, z coordinates) are in the final dataframe.
    Note: if some nodes do not have coordinates, they will be returned as nans
    """
    nodes = pd.DataFrame(map(lambda x: x[1], nxgraph.nodes.data()), index=list(nxgraph.nodes))
    for n in nodecols:
        if n not in nodes:
            raise ValueError('Node column variable ' + str(n) + ' is not in NetworkX input.')
    return nodes


def _networkx_edge_to_nodesdf(nxgraph, edgecols):
    """
    Takes networkx graph input and returns with the node information in dataframe format for netplotbrian.
    Returns the dataframe with the column names in .
    Any other attributes are included.
    Checks if all node_columnnames (i.e. x, y, z coordinates) are in the final dataframe.
    Note: if some nodes do not have coordinates, they will be returned as nans
    """
    edges = pd.DataFrame(map(lambda x: {edgecols[0]: x[0]} |
                                        {edgecols[1]: x[1]} |
                                        x[2], nxgraph.edges.data()))
    return edges


def _from_networkx_input(nxgraph, **kwargs):
    """
    Takes networkx input and outputs in two dataframee:
    nodes and edges.

    Edge names correspond to edgecolumnname keyword argument.
    Any additional edge attributes in the networkx get included in the output dataframe.

    Nodes require that node x, y, and z nodecolumnanmes to be included in the nxgraph attributes.
    Any additional node attributes in the networkx graph get included in the output dataframe
    """
    # Note: in the future, it is possible to expand/modify node_df to check if that includes x,y,z instead of networkx.
    # Get edge and node columnanmes
    edgecols = kwargs.get('edge_columnnames')
    nodecols = kwargs.get('node_columnnames')
    if nodecols == 'auto':
        nodecols = ['x', 'y', 'z']

    # Convert each of the properties in turn
    nodes = _networkx_nodes_to_nodesdf(nxgraph, nodecols)
    edges = _networkx_edge_to_nodesdf(nxgraph, edgecols)

    return nodes, edges