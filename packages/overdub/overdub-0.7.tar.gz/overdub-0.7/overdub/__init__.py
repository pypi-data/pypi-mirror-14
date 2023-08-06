from .bases import MutableOverdub, Overdub
from ._version import get_versions

__all__ = ['MutableOverdub', 'Overdub']
__version__ = get_versions()['version']
del get_versions
