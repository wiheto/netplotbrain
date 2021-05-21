"""Legend plots"""
import numpy as np
import matplotlib.cm as cm
from ..utils import _node_scale_vminvmax


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
    nodevminvmax = kwargs.get('nodevminvmax')
    if nodesizelegend is True:
        if isinstance(nodesize, str) and nodesize in nodes.columns:
            _, nl = _node_scale_vminvmax(
                nodes, nodesize, return_labels=True, **kwargs)
            # If nodevminvmax is set, use that as the smallest and largest size/labels
            # otherwise derive from data
            if isinstance(nodevminvmax, list):
                ns_min_legend = nodevminvmax[0]
                ns_max_legend = nodevminvmax[1]
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
        ax.text(x, 0.925, label, color='Gray', ha='center',
                font='Sawasdee', fontsize='xx-small')
    ax.text(np.mean(np.arange(len(nodesizelegendlabels))), 1.05, nodesize,
            color='Gray', ha='center', font='Sawasdee', fontsize='medium')
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
    uniquenodecolorby = set(nodes[nodecolorby].dropna().values)
    uniquenodecolors_idx = [nodes[nodes[nodecolorby] ==
                                  x].first_valid_index() for x in uniquenodecolorby]
    uniquenodecolors = nodecolor[uniquenodecolors_idx, :]
    ax.scatter(np.arange(len(uniquenodecolorby)), np.ones(
        len(uniquenodecolorby)), color=uniquenodecolors, s=nodescale)
    for x, label in enumerate(uniquenodecolorby):
        ax.text(x, 0.925, label, color='Gray', ha='center',
                font='Sawasdee', fontsize='xx-small')
    ax.set_ylim([0.85, 1.1])
    ax.set_xlim([-2, len(uniquenodecolorby) + 1])
    # Plot title
    ax.text(np.mean(np.arange(len(uniquenodecolorby))), 1.05, nodecolorby,
            color='Gray', ha='center', font='Sawasdee', fontsize='medium')
    return ax


def add_nodecolor_legend_continuous(ax, nodes, nodecolorby, nodecmap):
    """
    Add node color legend to bottom of figure.
    This is for continuous colours.
    """
    nc_min = nodes[nodecolorby].min()
    nc_max = nodes[nodecolorby].max()
    inc = (nc_max - nc_min) / 100
    imspan = np.arange(nc_min, nc_max + (inc / 2), inc)
    imsquare = np.outer(np.ones(1), imspan)
    ax.imshow(imsquare, cmap=cm.get_cmap(nodecmap),
              origin='lower', extent=(-3, 3, 1, 1.3))
    inc = (nc_max - nc_min) / 4
    xticklabels = np.arange(nc_min, nc_max + (inc / 2), inc)
    for i, xtick in enumerate(np.arange(-3, 3.01, 1.5)):
        ax.plot([xtick, xtick], [0.94, 0.99], linewidth=1, color='lightgray')
        ax.text(xtick, 0.75, np.round(xticklabels[i], 3), color='Gray', ha='center',
                font='Sawasdee', fontsize='xx-small', transform=ax.transData)
    # Plot title
    ax.text(0, 1.4, nodecolorby,
            color='Gray', ha='center', font='Sawasdee', fontsize='medium')
    return ax


def _add_nodecolor_legend(ax, nodes, nodecolorby, nodecolor, nodecmap, **kwargs):
    """
    Adds a nodecolor legend to figure.
    This function descites whether a discrete or continuous colorbar is to be added.
    """
    nodecolorlegendstyle = kwargs.get('nodecolorlegendstyle')
    # First a heuristic if nodecolorlegendstyle is not specified
    if nodecolorlegendstyle == 'auto' and nodes[nodecolorby].nunique() > 8:
        nodecolorlegendstyle = 'continuious'
    elif nodecolorlegendstyle == 'auto' and nodes[nodecolorby].nunique() <= 8:
        nodecolorlegendstyle = 'discrete'
    # Plot whichever legend is wanted
    if nodecolorlegendstyle == 'discrete':
        ax = _add_nodecolor_legend_discrete(
            ax, nodes, nodecolorby, nodecolor, **kwargs)
    else:
        ax = add_nodecolor_legend_continuous(ax, nodes, nodecolorby, nodecmap)

    return ax
