from __future__ import absolute_import
from PIL import Image
import numpy
import os
import glob


def import_png(png_filename):
    """
    Import a png file into a numpy array.

    Arguments:
        :png_filename:  A string filename of a png datafile

    Returns:
        A numpy array with data from the png file
    """

    # Expand filename to be absolute
    png_filename = os.path.expanduser(png_filename)

    try:
        img = Image.open(png_filename)
    except Exception as e:
        raise ValueError("Could not load file {0} for conversion."
                         .format(png_filename))
        raise

    return numpy.array(img)


def export_png(png_filename, numpy_data):
    """
    Export a numpy array to a png file.

    Arguments:
        png_filename:   A filename to which to save the png data
        numpy_data:     The numpy array to save to png. OR a string

    Returns:
        String. The expanded filename that now holds the png data
    """

    # Expand filename to be absolute
    png_filename = os.path.expanduser(png_filename)

    if type(numpy_data) is str:
        fp = open(png_filename, "wb")
        fp.write(numpy_data)
        fp.close()
        return png_filename

    try:
        if numpy_data.dtype.name != 'uint8':
            m = 'I'
            img = Image.fromarray(numpy_data, mode=m)
        else:
            img = Image.fromarray(numpy_data)
        img.save(png_filename)
    except Exception as e:
        raise ValueError("Could not save png file {0}.".format(png_filename))
    return png_filename


def export_png_collection(png_filename_base, numpy_data, start_layers_at=1):
    """
    Export a numpy array to a set of png files, with each Z-index 2D
    array as its own 2D file.

    Arguments:
        png_filename_base:     A filename template, such as "my-image-*.png"
                                which will lead to a collection of files named
                                "my-image-0.png", "my-image-1.png", etc.
        numpy_data:             The numpy array data to save to png.

    Returns:
        Array. A list of expanded filenames that hold png data.
    """

    file_ext = png_filename_base.split('.')[-1]
    if file_ext in ['png']:
        # Filename is "name*.tif[f]", set file_base to "name*".
        file_base = '.'.join(png_filename_base.split('.')[:-1])
    else:
        # Filename is "name*", set file_base to "name*".
        # That is, extension wasn't included.
        file_base = png_filename_base
        file_ext = ".png"

    file_base_array = file_base.split('*')

    # The array of filenames to return
    output_files = []

    # Filename 0-padding
    i = start_layers_at
    for layer in numpy_data:
        layer_filename = (str(i).zfill(6)).join(file_base_array) + file_ext
        output_files.append(export_png(layer_filename, layer))
        i += 1

    return output_files


def import_png_collection(png_filename_base):
    """
    Import all files matching the filename base given via `png_filename_base`.
    Images are ordered by alphabetical order, which means that you *MUST* 0-pad
    your numbers if they span a power of ten (e.g. 0999-1000 or 09-10). This is
    handled automatically by the complement function, `export_png_collection`.
    Also, look at how nicely these documentation lines are all the same length!

    Arguments:
        png_filename_base:     An asterisk-wildcard string that should refer
                                to all TIFFs in the stack. All * are replaced
                                according to command-line expansion rules.
    Returns:
        A numpy array holding a 3D dataset
    """

    # We expect images to be indexed by their alphabetical order.
    files = glob.glob(png_filename_base)
    files.sort()

    numpy_data = []
    for f in files:
        numpy_data.append(import_png(f))

    return numpy.concatenate(numpy_data)
