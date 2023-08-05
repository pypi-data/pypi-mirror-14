"DiskCache: disk and file-based cache."

from .core import Cache, Disk, EmptyDirWarning
from .core import LIMITS, DEFAULT_SETTINGS, EVICTION_POLICY
from .fanout import FanoutCache

try:
    from .djangocache import DjangoCache
except ImportError:
    # Django not installed so ignore.
    pass


__title__ = 'diskcache'
__version__ = '0.9.0'
__build__ = 0x000900
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Grant Jenks'
