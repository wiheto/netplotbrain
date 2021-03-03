from .plot_utils import _set_axes_equal, _set_axes_radius, _get_view
from .plot_edges import _plot_edges
from .plot_nodes import _scale_nodes, _plot_nodes
from .plot_spheres import _plot_spheres
from .plot_templates import _plot_template, _plot_template_style_filled, \
    _plot_template_style_cloudy, _plot_template_style_surface
from .plot_dimarrows import _add_axis_arrows
from .plot_parcels import _get_nodes_from_nii, _plot_parcels

__all__ = ['_set_axes_equal', '_set_axes_radius', '_get_view',
           '_plot_template', '_plot_template_style_filled',
           '_plot_template_style_cloudy',
           '_scale_nodes', '_plot_nodes', '_plot_spheres',
           '_plot_edges', '_plot_template_style_surface',
           '_add_axis_arrows', '_get_nodes_from_nii', '_plot_parcels']
