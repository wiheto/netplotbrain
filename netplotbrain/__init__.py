"""
.. include:: ../README.md

.. include:: ../docs/gallery.md
"""
from .plot import plot
from .__version import __version__
from .derive import edges_from_bids

__all__ = ['plot', '__version__', 'edges_from_bids']
__pdoc__ = {
    "plotting": False,
    "utils": False,
    "templatesettings": False,
}

