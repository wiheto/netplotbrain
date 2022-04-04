"""Main plotting functions in package."""
from .plot_edges import _plot_edges, _npedges2dfedges
from .plot_nodes import _scale_nodes, _plot_nodes, _select_single_hemisphere_nodes
from .plot_spheres import _plot_spheres
from .plot_templates import _plot_template, _plot_template_style_filled, \
    _plot_template_style_cloudy, _plot_template_style_surface
from .plot_dimarrows import _add_axis_arrows
from .plot_parcels import _get_nodes_from_nii, _plot_parcels
from .plot_title import _add_subplot_title
from .process_input import get_frame_input, _process_edge_input, _process_node_input,\
    _init_figure, _check_axinput
from .plot_legend import _add_nodecolor_legend, _add_nodesize_legend, _setup_legend
from .plot_gif import _plot_gif

__all__ = ['_plot_template', '_plot_template_style_filled',
           '_plot_template_style_cloudy',
           '_scale_nodes', '_plot_nodes', '_plot_spheres',
           '_plot_edges', '_plot_template_style_surface',
           '_add_axis_arrows', '_get_nodes_from_nii', '_plot_parcels',
           '_select_single_hemisphere_nodes', '_npedges2dfedges', '_add_subplot_title',
           '_setup_legend', '_process_edge_input', '_process_node_input', '_add_nodesize_legend',
           '_add_nodecolor_legend', 'get_frame_input', '_init_figure', '_check_axinput', '_plot_gif']
