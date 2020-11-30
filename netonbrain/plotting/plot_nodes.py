
def _plot_nodes(ax, nodes, affine=None, nodesize=50, nodecolor='salmon'):
    # Check if nodesize input is column in node data
    if isinstance(nodesize, str) and nodesize in nodes.columns:
        ns = nodes[nodesize]
    else:
        ns = nodesize
    # Set colormap
    nc = nodecolor
    ax.scatter(nodes['x'], nodes['y'], nodes['z'], s=ns, color=nc)

def _scale_nodes(nodes, affine=None):
    nodes_scaled = nodes.copy()
    if affine is not None:
        nodes_scaled['x'] = (nodes_scaled['x'] - affine[0, -1]) / affine[0, 0]
        nodes_scaled['y'] = (nodes_scaled['y'] - affine[1, -1]) / affine[1, 1]
        nodes_scaled['z'] = (nodes_scaled['z'] - affine[2, -1]) / affine[2, 2]
    return nodes_scaled
