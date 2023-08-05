"""
Classes for handling raster data.
"""

from . import grid
from . import aaigrid
from . import misc

from .grid import RegularGrid, WarpedGrid, merge
from .read import read_aai, read_gtiff, aairead, gtiffread
from .aaigrid import AAIGrid
from .misc import witch_of_agnesi, peaks, pad, slope, aspect, grad, div
from .misc import normed_vector_field
from .crfuncs import streamline2d

__all__ = ["grid", "aaigrid", "misc",
           "RegularGrid", "WarpedGrid",
           "aairead", "gtiffread", "read_aai", "read_gtiff",
           "AAIGrid",
           "pad", "slope", "aspect", "grad", "div", "normed_vector_field",
           "streamline2d"]

