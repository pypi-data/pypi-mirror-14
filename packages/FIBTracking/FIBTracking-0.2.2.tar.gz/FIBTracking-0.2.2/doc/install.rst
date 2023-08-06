Installation
============

Requirements
++++++++++++

The following dependencies are needed to run the code (as-written). Some of
these could be removed, but the code was written with my research
results in mind, and as such, has some dependencies that make things match
my personal preferences (such as ``seaborn``). Some details on installing them
are given below:

..  csv-table::
    :header: Package, Source, PyPI
    :escape: \

    ``numpy``, `Source <Numpy_>`_, `PyPI <NumpyPYPI_>`_
    ``Opencv``, `Source <OpenCV_>`_,
    ``PyQt4``, `Source <PyQt4_>`_,
    ``matplotlib``, `Source <matplotlib_>`_, `PyPI <matplotlibPYPI_>`_
    ``scikit-image``, `Source <skimage_>`_ , `PyPI <skimagePYPI_>`_
    ``tqdm``, `Source <tqdm_>`_, `PyPI <tqdmPYPI_>`_
    ``seaborn``, `Source <seaborn_>`_, `PyPI <seabornPYPI_>`_
    ``statsmodels``, `Source <statsmodels_>`_, `PyPI <statsmodels_>`_

.. _Numpy: http://www.numpy.org/
.. _NumpyPYPI: https://pypi.python.org/pypi/numpy/1.11.0
.. _matplotlib: http://matplotlib.org/
.. _matplotlibPYPI: https://pypi.python.org/pypi/matplotlib/1.5.1
.. _skimage: https://github.com/scikit-image/scikit-image
.. _skimagePYPI: https://pypi.python.org/pypi/scikit-image
.. _seaborn: https://stanford.edu/~mwaskom/software/seaborn/
.. _seabornPYPI: https://pypi.python.org/pypi/seaborn
.. _statsmodels: http://statsmodels.sourceforge.net/
.. _statsmodelsPYPI: https://pypi.python.org/pypi/statsmodels
.. _tqdm: https://github.com/tqdm/tqdm/
.. _tqdmPYPI: https://pypi.python.org/pypi/tqdm
.. _OpenCV: http://opencv.org/
.. _PyQt4: https://www.riverbankcomputing.com/software/pyqt/download


Development Version Installation
++++++++++++++++++++++++++++++++

Currently, only the development version is capable of installation.
The latest version of the code should be available in the online
`repository <https://jat255@bitbucket.org/jat255/fibtracking.git>`_.
To get this version installed on your system, clone the repository,
and then install with ``pip``:

.. code-block:: bash

    $ git clone https://jat255@bitbucket.org/jat255/fibtracking.git
    $ cd fibtracking
    $ pip install -e ./

