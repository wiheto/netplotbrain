"""Legend plots"""
import numpy as np
import matplotlib.cm as cm
from ..utils import _node_scale_vminvmax, _detect_nodecolor_type


def _setup_legend(legendproperty, legend, legendname, currentlegend=None):
    # If the condition has been specified
    # And if the legend for that legendproperty is true
    if isinstance(legendproperty, str) and legend is not False:
        # If currentlegend is None, initailize
        if currentlegend is None:
            currentlegend = []
        currentlegend += [legendname]
    return currentlegend


def _add_nodesize_legend(ax, nodes, nodesize, **kwargs):
    """
    Adds node size legend to bottom of figure
    """
    # Get relevant kwargs
    nodescale = kwargs.get('nodescale')
    nodesizelegend = kwargs.get('nodesizelegend')
    nodesizevminvmax = kwargs.get('nodesizevminvmax')
    font = kwargs.get('font')
    fontcolor = kwargs.get('fontcolor')
    legendtickfontsize = kwargs.get('legendtickfontsize')
    legendtitlefontsize = kwargs.get('legendtitlefontsize')
    if nodesizelegend is True:
        if isinstance(nodesize, str) and nodesize in nodes.columns:
            _, nl = _node_scale_vminvmax(
                nodes, nodesize, return_labels=True, **kwargs)
            # If nodesizevminvmax is set, use that as the smallest and largest size/labels
            # otherwise derive from data
            if isinstance(nodesizevminvmax, list):
                ns_min_legend = nodesizevminvmax[0]
                ns_max_legend = nodesizevminvmax[1]
            else:
                ns_min_legend = nl.min()
                ns_max_legend = nl.max()
            # NOTE If behaviour in node_scale_vminvax changes, then this needs to change too
            ns_min = 0.05 * nodescale
            ns_max = 1.05 * nodescale
            # TODO could add nodsizelegendtick here.
            inc = (ns_max - ns_min) / 4
            nodesizelegend = np.arange(ns_min, ns_max + inc, inc)
            legend_inc = (ns_max_legend - ns_min_legend) / 4
            nodesizelegendlabels = np.arange(
                ns_min_legend, ns_max_legend + legend_inc / 2, legend_inc)
            nodesizelegendlabels = nodesizelegendlabels.round(3)
        else:
            raise ValueError(
                'Unable to plot size legend (nodesize specification issue)')
    else:
        # This ensures input of nodelegendlabels is the unscaled unit.
        nodesizelegendlabels = np.array(nodesizelegend)
        nodesizelegend = np.array(nodesizelegendlabels) * nodescale

    ax.scatter(np.arange(len(nodesizelegend)), np.ones(
        len(nodesizelegend)), s=nodesizelegend, color='gray')
    for x, label in enumerate(nodesizelegendlabels):
        ax.text(x, 0.925, label, color=fontcolor, ha='center',
                font=font, fontsize=legendtickfontsize)
    ax.text(np.mean(np.arange(len(nodesizelegendlabels))), 1.05, nodesize,
            color=fontcolor, ha='center', font=font, fontsize=legendtitlefontsize)
    ax.set_ylim([0.925, 1.1])
    ax.set_xlim([-2, len(nodesizelegendlabels) + 1])
    return ax


def _add_nodecolor_legend_discrete(ax, nodes, nodecolorby, nodecolor, **kwargs):
    """
    Add node color legend to bottom of figure.
    This is for discrete colours.
    """
    # Get relevant kwargs
    nodescale = kwargs.get('nodescale')
    font = kwargs.get('font')
    fontcolor = kwargs.get('fontcolor')
    legendtickfontsize = kwargs.get('legendtickfontsize')
    legendtitlefontsize = kwargs.get('legendtitlefontsize')
    # Create list of discrete colors
    uniquenodecolorby = sorted(list(set(nodes[nodecolorby].dropna().values)))
    uniquenodecolors_idx = [nodes[nodes[nodecolorby] ==
                                  x].first_valid_index() for x in uniquenodecolorby]
    uniquenodecolors = nodecolor[uniquenodecolors_idx, :]
    ax.scatter(np.arange(len(uniquenodecolorby)), np.ones(
        len(uniquenodecolorby)), color=uniquenodecolors, s=nodescale)
    for x, label in enumerate(uniquenodecolorby):
        ax.text(x, 0.925, label, color=fontcolor, ha='center',
                font=font, fontsize=legendtickfontsize)
    ax.set_ylim([0.85, 1.1])
    ax.set_xlim([-2, len(uniquenodecolorby) + 1])
    # Plot title
    ax.text(np.mean(np.arange(len(uniquenodecolorby))), 1.05, nodecolorby,
            color=fontcolor, ha='center', font=font, fontsize=legendtitlefontsize)
    return ax


def add_nodecolor_legend_continuous(ax, nodes, nodecolorby, nodecmap, **kwargs):
    """
    Add node color legend to bottom of figure.
    This is for continuous colours.
    """
    # Get relevant kwargs
    font = kwargs.get('font')
    fontcolor = kwargs.get('fontcolor')
    legendtickfontsize = kwargs.get('legendtickfontsize')
    legendtitlefontsize = kwargs.get('legendtitlefontsize')
    nodecolorvminvmax = kwargs.get('nodecolorvminvmax')
    # Create continuous scale
    if nodecolorvminvmax == 'minmax':
        nc_min = nodes[nodecolorby].min()
        nc_max = nodes[nodecolorby].max()
    elif  nodecolorvminvmax == 'maxabs':
        nc_min = -nodes[nodecolorby].abs().max()
        nc_max = nodes[nodecolorby].abs().max()
    else:
        nc_min = nodecolorvminvmax[0]
        nc_max = nodecolorvminvmax[1]
    inc = (nc_max - nc_min) / 100
    imspan = np.arange(nc_min, nc_max + (inc / 2), inc)
    imsquare = np.outer(np.ones(1), imspan)
    ax.imshow(imsquare, cmap=cm.get_cmap(nodecmap),
              origin='lower', extent=(-3, 3, 1, 1.3))
    inc = (nc_max - nc_min) / 4
    xticklabels = np.arange(nc_min, nc_max + (inc / 2), inc)
    for i, xtick in enumerate(np.arange(-3, 3.01, 1.5)):
        ax.plot([xtick, xtick], [0.94, 0.99], linewidth=1, color='lightgray')
        ax.text(xtick, 0.75, np.round(xticklabels[i], 3), color=fontcolor, ha='center',
                font=font, fontsize=legendtickfontsize, transform=ax.transData)
    # Plot title
    ax.text(0, 1.4, nodecolorby,
            color=fontcolor, ha='center', font=font, fontsize=legendtitlefontsize)
    return ax


def _add_nodecolor_legend(ax, nodes, nodecolorby, nodecolor, nodecmap, **kwargs):
    """
    Adds a nodecolor legend to figure.
    This function descites whether a discrete or continuous colorbar is to be added.
    """
    nodecolorlegendstyle = kwargs.get('nodecolorlegendstyle')
    nodecolorlegendstyle = _detect_nodecolor_type(nodes, nodecolorby, nodecolorlegendstyle)
    # Plot whichever legend is wanted
    if nodecolorlegendstyle == 'discrete':
        ax = _add_nodecolor_legend_discrete(
            ax, nodes, nodecolorby, nodecolor, **kwargs)
    else:
        ax = add_nodecolor_legend_continuous(ax, nodes, nodecolorby, nodecmap, **kwargs)

    return ax
