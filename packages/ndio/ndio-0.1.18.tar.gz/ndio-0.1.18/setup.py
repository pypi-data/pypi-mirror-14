import ndio

VERSION = ndio.version
"""
update docs with:
sphinx-apidoc -f -o ./docs/source/ ./ndio *.py
cd docs
make html

roll with:

git tag VERSION
git push --tags
python setup.py sdist upload -r pypi
"""

from distutils.core import setup
setup(
    name = 'ndio',
    packages = [
        'ndio',
        'ndio.convert',
        'ndio.ramon',
        'ndio.remote',
        'ndio.utils'
    ],
    version = VERSION,
    description = 'A Python library for open neuroscience data access and manipulation.',
    author = 'Jordan Matelsky',
    author_email = 'jordan@neurodata.io',
    url = 'https://github.com/neurodata/ndio',
    download_url = 'https://github.com/neurodata/ndio/tarball/' + VERSION,
    keywords = [
        'brain',
        'medicine',
        'microscopy',
        'neuro',
        'neurodata',
        'neurodata.io',
        'neuroscience',
        'ndio',
        'ocpy',
        'ocp',
        'ocp.me',
        'connectome',
        'connectomics',
        'spatial',
        'EM',
        'MRI',
        'fMRI',
        'calcium'
    ],
    classifiers = [],
)
