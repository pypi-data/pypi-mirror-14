Introduction
============
This module is used to measure fiducial marks that have been etched in the top
of a FIB/SEM data cube, in order to get a measurement of how thick each slice
was. [#]_
When preparing a site for FIB/SEM nanotomography, mill or deposit some sort of
feature at a fixed angle on the top surface of the data volume.
When viewed in cross-section, those features will get closer together the
farther into the volume you mill. Utilizing the geometry of the situation,
an estimate for the slice thickness can be obtained by comparing
the distance between the two fiducials on subsequent slices.

It requires a `PyQt`_ and `OpenCV`_ installation in order to work, since a number
of the methods are graphical and interactive. Installation of these can be
a little tricky, but should be doable from the links given above.


.. _paper: `Introduction`_
.. _Avizo: http://www.fei.com/software/avizo3d/
.. _PyQt: https://riverbankcomputing.com/software/pyqt/intro
.. _OpenCV: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_intro/py_intro.html#intro
.. [#] https://www.google.com/patents/US8178838