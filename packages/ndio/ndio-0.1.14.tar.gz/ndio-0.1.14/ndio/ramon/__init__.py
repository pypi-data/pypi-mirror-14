from __future__ import absolute_import
import tempfile

from ndio.ramon.RAMONBase import *
from ndio.ramon.RAMONGeneric import *
from ndio.ramon.RAMONNeuron import *
from ndio.ramon.RAMONOrganelle import *
from ndio.ramon.RAMONSegment import *
from ndio.ramon.RAMONSynapse import *
from ndio.ramon.RAMONVolume import *

from .errors import *

"""

The enumerables in this file are to afford compatibility with CAJAL, which uses
integers as types. To convert from integer to string (for instance, if you want
to specify the ANNOTATION_TYPE in a RAMON hdf5 file), use:

    >>> AnnotationType.get_str(1)
    "GENERIC"

To convert from an integer to an actual RAMON type (say, if you want to create
a new RAMON object dynamically), use:

    >>> AnnotationType.get_class(1)
    ndio.ramon.RAMONGeneric.RAMONGeneric

So you can create a new RAMON object of dynamic type like this:

    >>> anno_type = 5
    >>> r = AnnotationType.get_class(anno_type)()
    >>> type(r)
    ndio.ramon.RAMONNeuron.RAMONNeuron

NOTE! If you already have an HDF5 file that contains a RAMON object, it is far
easier to use the prebuilt `hdf5_to_ramon()` function (below).

    >>> import h5py
    >>> f = h5py.File('myfile.hdf5', 'r')
    >>> r = hdf5_to_ramon(f)

"""

_types = {
    "generic": 1,
    "synapse": 2,
    "seed": 3,
    "segment": 4,
    "neuron": 5,
    "organelle": 6,
    "attributedregion": 7,
    "volume": 8
}

_reverse_types = {v: k for k, v in list(_types.items())}

_ramon_types = {
    _types["generic"]: RAMONGeneric,
    _types["synapse"]: RAMONSynapse,
    _types["seed"]:  None,
    _types["segment"]: RAMONSegment,
    _types["neuron"]: RAMONNeuron,
    _types["organelle"]: RAMONOrganelle,
    # _types["ATTRIBUTEDREGION"]: None,
    _types["volume"]: RAMONVolume
}

_reverse_ramon_types = {v: k for k, v in list(_ramon_types.items())}


class AnnotationType:
    GENERIC = _types["generic"]
    SYNAPSE = _types["synapse"]
    SEED = _types["seed"]
    SEGMENT = _types["segment"]
    NEURON = _types["neuron"]
    ORGANELLE = _types["organelle"]
    ATTRIBUTEDREGION = _types["attributedregion"]
    VOLUME = _types["volume"]

    @staticmethod
    def get_str(type):
        return _reverse_types[type]

    @staticmethod
    def get_class(type):
        return _ramon_types[type]

    @staticmethod
    def get_int(type):
        return _reverse_ramon_types[type]


def hdf5_to_ramon(hdf5, anno_id=None):
    """
    Converts an HDF5 file to a RAMON object. Returns an object that is a child-
    -class of RAMON (though it's determined at run-time what type is returned).

    Accessing multiple IDs from the same file is not supported, because it's
    not dramatically faster to access each item in the hdf5 file at the same
    time It's semantically and computationally easier to run this function
    several times on the same file.

    Arguments:
        hdf5 (h5py.File): A h5py File object that holds RAMON data
        anno_id (int): The ID of the RAMON obj to extract from the file. This
            defaults to the first one (sorted) if none is specified.

    Returns:
        ndio.RAMON object
    """

    if anno_id is None:
        # The user just wants the first item we find, so... Yeah.
        return hdf5_to_ramon(hdf5, list(hdf5.keys())[0])

    # First, get the actual object we're going to download.
    anno_id = str(anno_id)
    if anno_id not in list(hdf5.keys()):
        raise ValueError("ID {} is not in this file. Options are: {}".format(
            anno_id,
            ", ".join(list(hdf5.keys()))
        ))

    anno = hdf5[anno_id]
    # anno now holds just the RAMON of interest

    # This is the most complicated line in here: It creates an object whose
    # type is conditional on the ANNOTATION_TYPE of the hdf5 object.
    try:
        r = AnnotationType.get_class(anno['ANNOTATION_TYPE'][0])()
    except:
        raise InvalidRAMONError("This is not a valid RAMON type.")

    # All RAMON types definitely have these attributes:
    metadata = anno['METADATA']
    r.author = metadata['AUTHOR'][0]
    r.confidence = metadata['CONFIDENCE'][0]
    r.status = metadata['STATUS'][0]
    r.id = anno_id

    # These are a little tougher, some RAMON types have special attributes:

    if type(r) in [RAMONNeuron, RAMONSynapse]:
        r.segments = metadata['SEGMENTS'][()]

    if 'KVPAIRS' in metadata:
        kvs = metadata['KVPAIRS'][()][0].split()
        if len(kvs) != 0:

            for i in kvs:
                k, v = str(i).split(',')
                r.kvpairs[str(k)] = str(v)
        else:
            r.kvpairs = {}

    if issubclass(type(r), RAMONVolume):
        if 'CUTOUT' in anno:
            r.cutout = anno['CUTOUT'][()]
        if 'XYZOFFSET' in anno:
            r.cutout = anno['XYZOFFSET'][()]
        if 'RESOLUTION' in anno:
            r.cutout = anno['RESOLUTION'][()]

    if type(r) is RAMONSynapse:
        r.synapse_type = metadata['SYNAPSETYPE'][0]
        r.weight = metadata['WEIGHT'][0]

    if type(r) is RAMONSegment:
        if 'NEURON' in metadata:
            r.neuron = metadata['NEURON'][0]
        if 'PARENTSEED' in metadata:
            r.parent_seed = metadata['PARENTSEED'][0]
        if 'SEGMENTCLASS' in metadata:
            r.segment_class = metadata['SEGMENTCLASS'][0]
        if 'SYNAPSES' in metadata:
            r.synapses = metadata['SYNAPSES'][()]
        if 'ORGANELLES' in metadata:
            r.organelles = metadata['ORGANELLES'][()]

    if type(r) is RAMONOrganelle:
        r.organelle_class = metadata['ORGANELLECLASS'][0]

    return r


def ramon_to_hdf5(ramon, hdf5=None):
    """
    Exports a RAMON object to an HDF5 file object.

    Arguments:
        ramon (RAMON): A subclass of RAMONBase
        hdf5 (str): Export filename

    Returns:
        hdf5.File

    Raises:
        InvalidRAMONError: if you pass a non-RAMON object
    """

    if issubclass(type(ramon), RAMONBase) is False:
        raise InvalidRAMONError("Invalid RAMON supplied to ramon_to_hdf5.")

    import h5py
    import numpy

    if hdf5 is None:
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
    else:
        tmpfile = hdf5

    with h5py.File(tmpfile.name, "a") as hdf5:

        # First we'll export things that all RAMON objects have in
        # common, starting with the Group that encompasses each ID:
        grp = hdf5.create_group(str(ramon.id))

        grp.create_dataset("ANNOTATION_TYPE", (1,),
                           numpy.uint32,
                           data=AnnotationType.get_int(type(ramon)))
        if hasattr(ramon, 'resolution'):
            grp.create_dataset('RESOLUTION', (1,),
                               numpy.uint32, data=ramon.resolution)
        if hasattr(ramon, 'xyz_offset'):
            grp.create_dataset('XYZOFFSET', (3,),
                               numpy.uint32, data=ramon.xyz_offset)
        if hasattr(ramon, 'cutout'):
            grp.create_dataset('CUTOUT', ramon.cutout.shape,
                               ramon.cutout.dtype, data=ramon.cutout)

        # Next, add general metadata.
        metadata = grp.create_group('METADATA')

        metadata.create_dataset('AUTHOR', (1,),
                                dtype=h5py.special_dtype(vlen=str),
                                data=ramon.author)
        metadata.create_dataset('CONFIDENCE', (1,), numpy.float,
                                data=ramon.confidence)
        metadata.create_dataset('STATUS', (1,), numpy.uint32,
                                data=ramon.status)

        # Finally, add type-specific metadata:

        if hasattr(ramon, 'segments'):
            metadata.create_dataset('SEGMENTS',
                                    data=numpy.ndarray(ramon.segments))

        if hasattr(ramon, 'synapse_type'):
            metadata.create_dataset('SYNAPSETYPE', (1,), numpy.uint32,
                                    data=ramon.synapse_type)

        if hasattr(ramon, 'weight'):
            metadata.create_dataset('WEIGHT', (1,),
                                    numpy.float, data=ramon.weight)

        if hasattr(ramon, 'neuron'):
            metadata.create_dataset('NEURON', (1,),
                                    numpy.uint32, data=ramon.neuron)

        if hasattr(ramon, 'segment_class'):
            metadata.create_dataset('SEGMENTCLASS', (1,), numpy.uint32,
                                    data=ramon.segment_class)

        if hasattr(ramon, 'synapses'):
            metadata.create_dataset('SYNAPSES', (len(ramon.synapses),),
                                    numpy.uint32, data=ramon.synapses)

        if hasattr(ramon, 'organelles'):
            metadata.create_dataset('ORGANELLES',
                                    (len(ramon.organelles),),
                                    numpy.uint32,
                                    data=ramon.organelles)

        if hasattr(ramon, 'organelle_class'):
            metadata.create_dataset('ORGANELLECLASS', (1,),
                                    numpy.uint32,
                                    data=ramon.organelle_class)

        return tmpfile
    return False
