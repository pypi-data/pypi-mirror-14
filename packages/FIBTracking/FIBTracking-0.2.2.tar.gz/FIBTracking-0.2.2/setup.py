# Copyright 2016 Joshua Taillon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path
import io
import sys
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# next two methods read version from file
def read(*names, **kwargs):
    with io.open(
        path.join(path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

try:
    # noinspection PyUnresolvedReferences
    import cv2
except ImportError as e:
    sys.stderr.write(
        "\n**************************************************************\n"
        "FIBTracking requires OpenCV 3.0+ to be installed, which is not\n"
        "available with pip. Please install externally through your package\n"
        "manager. Windows users can try to use the packages here:\n"
        "http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv\n"
        "**************************************************************")
    sys.stderr.write('\n\n')
    sys.stderr.flush()
    # raise ImportError

setup(
    name='FIBTracking',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=find_version('fibtracking.py'),

    description='Python module for FIB/SEM fiducial tracking',
    long_description='This package provides methods to track fiducial marks '
                     'between subsequent slices in a nanotomography run from'
                     'the FIB-SEM and allows for calculation of slice '
                     'thickness based on these fiducials.',

    # The project's main homepage.
    url='https://bitbucket.org/jat255/jat255-python-modules/src/master/FIB-SEM/fibtracking/',

    # Author details
    author='Joshua Taillon',
    author_email='jat255@gmail.com',

    # Choose your license
    license='apache',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='electronmicroscopy fiducial FIB/SEM',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here. These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    extras_require={
        'full': ['numpy',
                 'matplotlib',
                  'statsmodels',
                  'seaborn',
                  'tqdm',
                  'scikit-image'],
        'base': [],
    },
)
