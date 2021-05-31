"""
.. include:: ../README.md

.. include:: ../docs/gallary.md
.. include:: ../docs/kwargs.rst
"""
from .plot import plot

__all__ = ['plot']
__pdoc__ = {
    "plotting": False,
    "utils": False,
    "templatesettings": False,
}