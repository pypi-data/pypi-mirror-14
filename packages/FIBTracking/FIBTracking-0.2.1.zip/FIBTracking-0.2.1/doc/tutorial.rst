Tutorial
========

This tutorial will run through how to load a FIB/SEM image stack,
identify two fiducials, track them from slice to slice to see how they change,
and get a measurement of

Getting Started
+++++++++++++++

#.  Download the image files for the tutorial and extract them to a folder.
    They can be found `here <https://umd.box.com/shared/static/zypc0boalvrrjphfxim42632mjjgdejh.zip>`_
    (719 MB download).

#.  Install the dependencies and the :mod:`~fibtracking.fibtracking` module
    following the :doc:`install` instructions.

#.  Fire up a Python (or Jupyter or Notebook) instance, and import the module
    (along with ``matplotlib`` if you are using Jupyter):

    ..  code-block:: python

        >>> %matplotlib qt4
        >>> from fibtracking import fibtracking as ft

Loading and Reviewing Images
++++++++++++++++++++++++++++

#.  Run the following code to load the images into memory. The
    :py:meth:`~fibtracking.fibtracking.readimages` method will pop-up a window
    asking for the directory containing the images. Click OK once you have chosen.

    .. code-block:: python

        >>> images = ft.readimages()
            Reading 308 images from C:\tmp\TiffImages:

#.  The :mod:`~fibtracking.fibtracking` module provides a simple interactive
    image browser using OpenCV tools. It can be invoked using the
    :py:meth:`~fibtracking.fibtracking.image_browser` method, and controlled
    using the keyboard shortcuts included in the title bar. Options are provided
    for labeling the image stack with the image index, as well as making the
    images smaller for easier viewing.

    ..  code-block:: python

        >>> ft.image_browser(images,
        ...                  downsize=True,
        ...                  labelimages=True)

    .. figure:: image_browser.png
       :width: 500 px
       :alt: FIBTracking Image Browser
       :align: center

#.  Similarly, there is an :py:meth:`~fibtracking.fibtracking.export_video`
    method that will use ``OpenCV``'s video export capability to save
    the image stack as an animated video. This method is somewhat brittle
    and the codec support is different on every machine (depending on how OpenCV
    was compiled), but I've been able to get it working on both Windows and
    Linux systems.

    Call the method giving the image list, a file name, and the frame rate
    (among some other options, similar to :py:meth:`~fibtracking.fibtracking.image_browser`):
    If no value is given for ``fourcc``, it should open a window asking for which
    codec to use. On Windows, the `Microsoft Video 1` codec seems to work best.
    On Linux, any supported codec should work.

    ..  code-block:: python

        >>> fibtracking.export_video(im_list=images,
        ...                          filename='test_video.avi',
        ...                          fps=20,
        ...                          labelimages=False)


    The method will also suggest an |ffmpeg|_ call that can be used to reduce
    the resulting file size (for sharing with others).
    This results in an output like the following:

    .. raw:: html

        <iframe width="500" height="400" align="center" src="https://www.youtube.com/embed/XJjNLsiu2jE" frameborder="1" allowfullscreen></iframe>


..  |ffmpeg| replace:: ``ffmpeg``
..  _ffmpeg: https://www.ffmpeg.org/


Tracking Fiducials
++++++++++++++++++

#.  Importantly, the module needs to know how big a pixel is in the horizontal
    dimension. As I have experience with FEI and Tescan FIB/SEM systems, support
    for reading this value from those files is implemented. For FEI, the value
    is read directly from the image. For Tescan, it is read from the header file
    that is saved with every outputted image:

    ..  code-block:: python

        >>> pixWidth = ft.get_tescan_pixel_width('slice-00001-png.hdr')
        ... # this image is not provided in the dataset, and is just for illustration purposes
        >>> print(pixWidth)
            2.4002e-08

        >>> pixWidth = ft.get_fei_pixel_width('EBeam - SliceImage - 001.tif')
        >>> print(pixWidth)
            2.13166e-08

#.  With the pixel width known, we can track fiducials now using the
    :py:meth:`~fibtracking.fibtracking.trackfiducials` method. See the documentation
    for details. Most important is the ``im_number`` parameter. It controls
    what image is displayed for selecting the fiducial (useful if the fiducials
    do not appear in the first few slices of your stack).

    ..  code-block:: python

        >>> widths = ft.trackfiducials(pix_width=pixWidth,
        ...                            im_list=images,
        ...                            im_number=20,
        ...                            plot_fiducials=True
        ...                            fid_num_to_plot=25,
        ...                            per_row=5)

#.  This method will prompt for a directory to read if no ``im_list`` is given.
    Otherwise, it pops up some instruction boxes that explain what you should
    do at each step:

    a.  The first step is to crop the data to the area to where you expect to see the
        fiducials. Since the fiducials should always be in the same general
        location, reducing the search area drastically speeds the fiducial
        recognition step. Keep in mind that the fiducials usually move upwards
        over the course of the acquisition, so make sure to select a large
        enough box to include them all.
        Press ``Enter`` after selecting the rectangle:

        ..  figure:: tracking1.png
            :width: 45%
            :alt: Selecting reduced area for fiducial search
            :align: center

    b.  In the next two dialogs, select a small box around the two fiducials
        to track.

        ..  image:: tracking2.png
            :width: 47%
            :alt: Selecting left fiducial

        ..  image:: tracking3.png
            :width: 47%
            :alt: Selecting right fiducial
        |
    c.  During operation, a progress bar will be shown to display how long the
        tracking is expected to take:

        ..  code-block:: python

            >>> widths = ft.trackfiducials(pix_width=pixWidth,
            ...                            im_list=images,
            ...                            im_number=20,
            ...                            plot_fiducials=True
            ...                            fid_num_to_plot=25,
            ...                            per_row=5)
                Pixel width is 2.13166e-08m
                Box coordinates are(x1, y1), (x2, y2): (470, 356), (1718, 870)
                Tracking fiducials:  41%|████      | 126/308 [00:08<00:12, 30.5 it/s]

    d.  If requested, plots showing where the fiducial was located in a range
        of images will be shown. If any of these are obviously not what you
        selected as a fiducial, there was some sort of problem with the recognition
        process and you should probably try again:

        ..  figure:: tracking_left.png
            :width: 500px
            :align: center
            :alt: Fiducial recognition



Visualizing Fiducial Tracking Data
++++++++++++++++++++++++++++++++++

#.  After running the last step, the ``widths`` variable should contain a list
    of distances (in whatever units ``pixWidth`` was given in) between
    the two fiducials recognized on each slice. These should get smaller
    as the list progresses, representing the fiducials getting closer together.

    A helper function is available to plot the this data:

    ..  code-block:: python

        >>> f = ft.plot_fid_distances(widths)

    ..  figure::    fid_width_plot.png
        :width:     500px
        :align:     center
        :alt:       Widths between recognized fiducials

    As can be observed, the first few slices are not particularly evenly spaced,
    but the milling reaches an equilibrium point and the profile eventually
    becomes linear around slice 70, meaning that the slice thicknesses
    are effectively equal.

    The :py:meth:`~fibtracking.fibtracking.plot_fid_distances` can also take a
    parameter ``plot_diff=True``, which will include a plot of the differences
    in fiducial widths between each slice. Due to the discrete nature
    of the data, this plot is not the most useful (and could probably use some
    improvements). Regardless, the output looks like this:

        ..  code-block:: python

            >>> f = ft.plot_fid_distances(widths, plot_diff=True)

    ..  figure::    fid_width_plot_w_deriv.png
        :width:     500px
        :align:     center
        :alt:       Widths between recognized fiducials with differences


Calculating Slice Thicknesses
+++++++++++++++++++++++++++++

.. _global-label:

Global Slice Thickness
^^^^^^^^^^^^^^^^^^^^^^

#.  Oftentimes, rather than an individual thickness value for each slice,
    the most relevant information is a global `average` slice thickness, and
    the range over which it is valid. The
    :py:meth:`~fibtracking.fibtracking.fit_fid_distances` method will help find
    this information.

        ..  code-block:: python

            >>> ft.fit_fid_distances(widths,
            ...                      start_image=110,
            ...                      fid_line_angle=40,
            ...                      reject_m=None,
            ...                      plot_results=True)
                Average fiducial delta_x is -33.39 nm
                Fiducial delta_x offset is 18718.21 nm
                Average slice thickness is 19.90 nm

    This method will plot the widths (similar to :py:meth:`~fibtracking.fibtracking.plot_fid_distances`),
    but will also fit a linear function to the data, and calculate an average
    slice thickness, based off of the ``fid_line_angle`` value provided.
    If the ``reject_m`` parameter is provided, the method will attempt to remove
    outlier data points (useful if the fiducial recognition was not perfect)
    before fitting, in order to give a more accurate value. The ``start_image``
    and ``end_image`` parameters can be used to tailor the range of slices
    used for fitting (useful for ignoring the first `N` slices that are not
    in equilibrium yet). If the ``plot_results`` flag is set, an output like
    the following will be produced:

    ..  figure::    fitted_distance_between_fiducials.png
        :width:     700px
        :align:     center
        :alt:       Fitted fiducial widths and average slice thickness

    In this dataset, we called for a nominal slice thickness of 20nm, and we
    can observe that on average, we were very close to that. In further processing,
    we can trim the first 75 slices (or so) off of our dataset to ensure
    we have uniform slice thicknesses, and set the thickness to 19.9nm.


Individual Slice Thicknesses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Although it has not been as useful as the :ref:`global-label` calculation,
    originally the methods were written to calculate individual slice thicknesses,
    and then trying to fit that data. As mentioned previously, the discrete
    nature of the data makes this information not terribly useful, but this
    is how you'd do it if you desire:

    ..  code-block:: python

        >>> thicknesses = ft.slice_thickness(widths,
        ...                                  fid_line_angle=40,
        ...                                  input_units='m',
        ...                                  output_units='nm')[0]

    The :py:meth:`~fibtracking.fibtracking.slice_thickness` method returns three
    values: the list of thicknesses, the mean, and the standard deviation, so we
    use the ``[0]`` syntax to extract just the list of thickness values.
    There is a :py:meth:`~fibtracking.fibtracking.plot_thicknesses` method to
    smooth this data and plot the results for exploration as well. The method
    has a great number of options for tailoring the output, and experimenting
    with these will be left as an exercise to the reader. A simple call:

    ..  code-block:: python

        >>> ft.plot_thicknesses(thicknesses, legend_loc='upper left')

    Produces output like the following. Included in this plot are some basic
    statistics (mean and standard deviation), as well as a `LOWESS`_ regression
    that helps show how the slice thickness is changing on average:

    ..  figure::    ind_thicknesses.png
        :width:     700px
        :align:     center
        :alt:       Individual slice thicknesses

    Again, if we crop out the first slices where there was no equilibrium,
    the results of the fit improve significantly:

    ..  code-block:: python

        >>> ft.plot_thicknesses(thicknesses[80:], legend_loc='upper left')

    ..  figure::    ind_thicknesses2.png
        :width:     700px
        :align:     center
        :alt:       Individual slice thicknesses (cropped list)


.. _LOWESS: http://statsmodels.sourceforge.net/devel/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html#statsmodels.nonparametric.smoothers_lowess.lowess


Saving/Importing Results
+++++++++++++++++++++++++

#.  For later or further analysis, the results of these methods can be easily
    saved to or imported from ``.csv`` files using the
    :py:meth:`~fibtracking.fibtracking.save_output` and
    :py:meth:`~fibtracking.fibtracking.import_csv_data` methods.

    To save the fiducial widths and slice thickness results:

    ..  code-block:: python

        >>> ft.save_output(widths,
        ...                fname='fiducial_widths.csv',
        ...                collabels=['Slice', 'Fiducial widths (m)'])
            2016-04-06 12:12:04
            Wrote output to fiducial_widths.csv
        >>> ft.save_output(thicknesses,
        ...                fname='thicknesses.csv',
        ...                collabels=['Slice','Thickness (nm)'])
            2016-04-06 12:13:42
            Wrote output to thicknesses.csv

    To import this data back into the program:

    ..  code-block:: python

        >>> widths = ft.import_csv_data('fiducial_widths.csv')
        >>> thicknesses = ft.import_csv_data('thicknesses.csv')

