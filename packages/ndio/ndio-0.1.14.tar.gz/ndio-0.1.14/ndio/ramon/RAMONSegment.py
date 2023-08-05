from __future__ import absolute_import
from .enums import *
from .errors import *
import numpy

from .RAMONVolume import RAMONVolume


class RAMONSegment(RAMONVolume):
    """
    RAMONSegment Object for storing neuroscience data with a voxel volume
    """
    def __init__(self,
                 segment_class=0,
                 neuron=0,
                 synapses=[],
                 organelles=[],

                 xyz_offset=(0, 0, 0),
                 resolution=0,
                 cutout=None,
                 voxels=None,

                 id=DEFAULT_ID,
                 confidence=DEFAULT_CONFIDENCE,
                 kvpairs=DEFAULT_DYNAMIC_METADATA,
                 status=DEFAULT_STATUS,
                 author=DEFAULT_AUTHOR):

            self.segment_class = segment_class
            self.neuron = neuron
            self.synapses = synapses
            self.organelles = organelles

            RAMONVolume.__init__(self,
                                 xyz_offset=xyz_offset,
                                 resolution=resolution,
                                 cutout=cutout,
                                 voxels=voxels,
                                 id=id,
                                 confidence=confidence,
                                 kvpairs=kvpairs,
                                 status=status,
                                 author=author)
