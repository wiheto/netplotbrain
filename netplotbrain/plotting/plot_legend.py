"""Legend plots"""
import numpy as np
import matplotlib.cm as cm
from ..utils import _node_scale_vminvmax, _detect_coloring_type


def _setup_legend(legendproperty, legend, legendname, currentlegend=None):
    # If the condition has been specified
    # And if the legend for that legendproperty is true
    if isinstance(legendproperty, str) and legend is not False:
        # If currentlegend is None, initailize
        if currentlegend is None:
            currentlegend = []
        currentlegend += [legendname]
    return currentlegend


def _add_node_size_legend(ax, nodes, node_size, **kwargs):
    """
    Adds node size legend to bottom of figure
    """
    # Get relevant kwargs
    node_scale = kwargs.get('node_scale')
    node_sizelegend = kwargs.get('node_sizelegend')
    node_sizevminvmax = kwargs.get('node_sizevminvmax')
    font = kwargs.get('font')
    fontcolor = kwargs.get('fontcolor')
    legend_tickfontsize = kwargs.get('legend_tickfontsize')
    legendtitle_fontsize = kwargs.get('legendtitle_fontsize')
    if node_sizelegend is True:
        if isinstance(node_size, str) and node_size in nodes.columns:
            _, nl = _node_scale_vminvmax(
                nodes, node_size, return_labels=True, **kwargs)
            # If node_sizevminvmax is set, use that as the smallest and largest size/labels
            # otherwise derive from data
            if isinstance(node_sizevminvmax, list):
                ns_min_legend = node_sizevminvmax[0]
                ns_max_legend = node_sizevminvmax[1]
            else:
                ns_min_legend = nl.min()
                ns_max_legend = nl.max()
            # NOTE If behaviour in node_scale_vminvax changes, then this needs to change too
            ns_min = 0.05 * node_scale
            ns_max = 1.05 * node_scale
            # TODO could add nodsizelegendtick here.
            inc = (ns_max - ns_min) / 4
            node_sizelegend = np.arange(ns_min, ns_max + inc, inc)
            legend_inc = (ns_max_legend - ns_min_legend) / 4
            node_sizelegendlabels = np.arange(
                ns_min_legend, ns_max_legend + legend_inc / 2, legend_inc)
            node_sizelegendlabels = node_sizelegendlabels.round(3)
        else:
            raise ValueError(
                'Unable to plot size legend (node_size specification issue)')
    else:
        # This ensures input of nodelegendlabels is the unscaled unit.
        node_sizelegendlabels = np.array(node_sizelegend)
        node_sizelegend = np.array(node_sizelegendlabels) * node_scale

    ax.scatter(np.arange(len(node_sizelegend)), np.ones(
        len(node_sizelegend)), s=node_sizelegend, color='gray')
    for x, label in enumerate(node_sizelegendlabels):
        ax.text(x, 0.925, label, color=fontcolor, ha='center',
                font=font, fontsize=legend_tickfontsize)
    ax.text(np.mean(np.arange(len(node_sizelegendlabels))), 1.05, node_size,
            color=fontcolor, ha='center', font=font, fontsize=legendtitle_fontsize)
    ax.set_ylim([0.925, 1.1])
    ax.set_xlim([-2, len(node_sizelegendlabels) + 1])
    return ax


def _add_node_color_legend_discrete(ax, nodes, node_colorby, node_color, **kwargs):
    """
    Add node color legend to bottom of figure.
    This is for discrete colours.
    """
    # Get relevant kwargs
    node_scale = kwargs.get('node_scale')
    font = kwargs.get('font')
    fontcolor = kwargs.get('fontcolor')
    legend_tickfontsize = kwargs.get('legend_tickfontsize')
    legendtitle_fontsize = kwargs.get('legendtitle_fontsize')
    # Create list of discrete colors
    uniquenode_colorby = sorted(list(set(nodes[node_colorby].dropna().values)))
    uniquenode_colors_idx = [nodes[nodes[node_colorby] ==
                                  x].first_valid_index() for x in uniquenode_colorby]
    uniquenode_colors = node_color[uniquenode_colors_idx, :]
    ax.scatter(np.arange(len(uniquenode_colorby)), np.ones(
        len(uniquenode_colorby)), color=uniquenode_colors, s=node_scale)
    for x, label in enumerate(uniquenode_colorby):
        ax.text(x, 0.925, label, color=fontcolor, ha='center',
                font=font, fontsize=legend_tickfontsize)
    ax.set_ylim([0.85, 1.1])
    ax.set_xlim([-2, len(uniquenode_colorby) + 1])
    # Plot title
    ax.text(np.mean(np.arange(len(uniquenode_colorby))), 1.05, node_colorby,
            color=fontcolor, ha='center', font=font, fontsize=legendtitle_fontsize)
    return ax


def add_node_color_legend_continuous(ax, nodes, node_colorby, **kwargs):
    """
    Add node color legend to bottom of figure.
    This is for continuous colours.
    """
    # Get relevant kwargs
    font = kwargs.get('font')
    fontcolor = kwargs.get('fontcolor')
    node_cmap = kwargs.get('node_cmap')
    legend_tickfontsize = kwargs.get('legend_tickfontsize')
    legendtitle_fontsize = kwargs.get('legendtitle_fontsize')
    node_colorvminvmax = kwargs.get('node_colorvminvmax')
    # Create continuous scale
    if node_colorvminvmax == 'minmax':
        nc_min = nodes[node_colorby].min()
        nc_max = nodes[node_colorby].max()
    elif  node_colorvminvmax == 'maxabs':
        nc_min = -nodes[node_colorby].abs().max()
        nc_max = nodes[node_colorby].abs().max()
    else:
        nc_min = node_colorvminvmax[0]
        nc_max = node_colorvminvmax[1]
    inc = (nc_max - nc_min) / 100
    imspan = np.arange(nc_min, nc_max + (inc / 2), inc)
    imsquare = np.outer(np.ones(1), imspan)
    ax.imshow(imsquare, cmap=cm.get_cmap(node_cmap),
              origin='lower', extent=(-3, 3, 1, 1.3))
    inc = (nc_max - nc_min) / 4
    xticklabels = np.arange(nc_min, nc_max + (inc / 2), inc)
    for i, xtick in enumerate(np.arange(-3, 3.01, 1.5)):
        ax.plot([xtick, xtick], [0.94, 0.99], linewidth=1, color='lightgray')
        ax.text(xtick, 0.75, np.round(xticklabels[i], 3), color=fontcolor, ha='center',
                font=font, fontsize=legend_tickfontsize, transform=ax.transData)
    # Plot title
    ax.text(0, 1.4, node_colorby,
            color=fontcolor, ha='center', font=font, fontsize=legendtitle_fontsize)
    return ax


def _add_node_color_legend(ax, nodes, node_colorby, node_color, **kwargs):
    """
    Adds a node_color legend to figure.
    This function descites whether a discrete or continuous colorbar is to be added.
    """
    node_colorlegendstyle = kwargs.get('node_colorlegendstyle')
    node_colorlegendstyle = _detect_coloring_type(nodes, node_colorby, node_colorlegendstyle)
    # Plot whichever legend is wanted
    if node_colorlegendstyle == 'discrete':
        ax = _add_node_color_legend_discrete(
            ax, nodes, node_colorby, node_color, **kwargs)
    elif node_colorlegendstyle == 'continuous':
        ax = add_node_color_legend_continuous(ax, nodes, node_colorby, **kwargs)

    return ax
