"""
.. include:: ../README.md

.. include:: ../docs/gallery.md
"""
from .plot import plot
from .__version import __version__

__all__ = ['plot', '__version__']
__pdoc__ = {
    "plotting": False,
    "utils": False,
    "templatesettings": False,
}

