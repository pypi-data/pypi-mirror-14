"""
Pyjo - Namespace package
========================
::

    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

:mod:`Pyjo` is namespace package that may be split across multiple project distributions.
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
