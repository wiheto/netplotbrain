"""Legend plots"""
import numpy as np
from ..plotting import _add_subplot_title
from ..utils import _node_scale_vminvmax


def _setup_legend(property, legend, legendname, currentlegend=None):
    # If the condition has been specified
    # And if the legend for that property is true
    if isinstance(property, str) and legend != False:
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
            ns, nl = _node_scale_vminvmax(nodes, nodesize, return_labels=True, **kwargs)
            # If nodevminvmax is set, use that as the smallest and largest size/labels
            # otherwise derive from data
            print(nodevminvmax)
            if isinstance(nodevminvmax, list):
                ns_min_legend = nodevminvmax[0]
                ns_max_legend = nodevminvmax[1]
            else:
                ns_min_legend = nl.min()
                ns_max_legend = nl.max()
            # NOTE If behaviour in node_scale_vminvax changes, then this needs to change too
            ns_min = 0.1 * nodescale
            ns_max = 1.1 * nodescale
            print(ns_min)
            print(ns_min_legend)
            print(ns_max)
            print(ns_max_legend)
            # TODO could add nodsizelegendtick here.
            inc = (ns_max - ns_min) / 4
            nodesizelegend = np.arange(ns_min, ns_max + inc, inc)

            legend_inc = (ns_max_legend - ns_min_legend) / 4
            nodesizelegendlabels = np.arange(ns_min_legend, ns_max_legend + legend_inc/2, legend_inc)
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


def _add_nodecolor_legend(ax, nodes, nodecolorby, nodecolor, **kwargs):
    """
    Add node color legend to bottom of figure
    """
    # Get relevant kwargs
    nodescale = kwargs.get('nodescale')
    uniquenodecolorby = set(nodes[nodecolorby].values)
    uniquenodecolors_idx = [nodes[nodes[nodecolorby] ==
                                  x].first_valid_index() for x in uniquenodecolorby]
    uniquenodecolors = nodecolor[uniquenodecolors_idx, :]
    ax.scatter(np.arange(len(uniquenodecolorby)), np.ones(
        len(uniquenodecolorby)), color=uniquenodecolors, s=nodescale)
    for x, label in enumerate(uniquenodecolorby):
        ax.text(x, 0.925, label, color='Gray', ha='center',
                font='Sawasdee', fontsize='xx-small')
    ax.text(np.mean(np.arange(len(uniquenodecolorby))), 1.05, nodecolorby,
            color='Gray', ha='center', font='Sawasdee', fontsize='medium')
    ax.set_ylim([0.925, 1.1])
    ax.set_xlim([-2, len(uniquenodecolorby) + 1])
    return ax
