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

__version__ = '0.2.1'

import os
import sys

os.environ['QT_API'] = 'pyqt'
backend = "qt4agg"

import cv2
import numpy as np
import matplotlib
from skimage.feature import peak_local_max
from tqdm import tqdm

matplotlib.rcParams['backend'] = backend
import matplotlib.pyplot as plt

matplotlib.pyplot.switch_backend(backend)

from PyQt4 import QtCore, QtGui


__all__ = ['get_filepaths',
           'readimages',
           'get_fei_pixel_width',
           'get_tescan_pixel_width',
           'trackfiducials',
           'plot_fid_distances',
           'fit_fid_distances',
           'image_browser',
           'export_video',
           'slice_thickness',
           'plot_thicknesses',
           'save_output',
           'import_csv_data',
           '_convert_units',
           ]


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    (From http://stackoverflow.com/a/19308592/1435788)

    Parameters
    ----------
    directory: str
        directory to walk and find files in
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(str(directory)):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths


def readimages():
    """
    Open a Qt dialog to get a directory and read all the .tif images inside of
    it with OpenCV

    Returns
    ------
    List of images read by opencv

    """
    # noinspection PyArgumentList
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)

    # noinspection PyTypeChecker
    directory = QtGui.QFileDialog.getExistingDirectory(
        None, "Select folder containing images", os.path.curdir)

    if len(directory) is 0:
        raise ValueError("No directory chosen. Cancelling.")

    # Do this with a loop so we can use a progress bar:

    # Get all things (directories and files in the directory)
    file_list = np.sort(get_filepaths(directory))

    # Filter out everything but .tif files from this list
    files = [v for v in file_list if v.endswith("tif")]

    # Try .png files if there are no tifs
    if len(files) is 0:
        files = [v for v in file_list if v.endswith("png")]

    # Raise exception if no image files found
    if len(files) is 0:
        raise ValueError("No .tif or .png images found in " + directory)

    # Pre-allocate im_list
    im_list = [0] * len(files)

    print("Reading " + repr(len(files)) + " images from " + directory + ":")
    sys.stdout.flush()

    # noinspection PyArgumentList
    # widgets = [Percentage(), ' ', Bar(), ' ', ETA()]
    # p = ProgressBar(len(im_list), widgets=widgets)

    for i, im_name in enumerate(tqdm(files, desc='Reading images')):
        im_list[i] = cv2.cvtColor(cv2.imread(im_name), cv2.COLOR_BGR2GRAY)

    return im_list


def get_fei_pixel_width(fname):
    """
    Get the width of a pixel (in nm) from an FEI tif file. Similar
    to how we used to use ``egrep -a`` previously, but this is just Python
    so it's simpler.

    Parameters
    ----------
    fname: string
        Filename of image to read from

    Returns
    -------
    pixWidth: float
        Width of the pixel (in nm)
    """
    import re
    f = open(fname, "rb")

    for line in f:
        if re.search(b'PixelWidth', line):
            res = line
            break

    if res is None:
        raise IndexError('Pixel width not found in image file')

    pixwidth = float(res.decode('ascii').split('=')[1].split('\r')[0])

    return pixwidth


def get_tescan_pixel_width(fname):
    """
    Get the width of a pixel (in nm) from a Tescan .hdr file. Similar
    to how we used to use ``egrep -a`` previously, but this is just Python
    so it's simpler.

    Parameters
    ----------
    fname: string
        Filename of image to read from

    Returns
    -------
    pixWidth: float
        Width of the pixel (in nm)
    """
    import re
    f = open(fname, "r")

    for line in f:
        if re.search('PixelSizeX', line):
            res = line
            break

    if res is None:
        raise IndexError('Pixel width not found in image file')

    pixwidth = float(res.split('=')[1].split('\r')[0])

    return pixwidth


def trackfiducials(pix_width,
                   im_list=None,
                   im_number=0,
                   plot_fiducials=False,
                   fid_num_to_plot=25,
                   per_row=5,
                   ):
    """
    Find distance between fiducial marks in image list

    Parameters
    ----------
    pix_width : float
        horizontal pixel width (in m)
        can be easily obtained by running `egrep -a PixelWidth
        <img filename> | tail -n 1` or using

    im_list : list of cv2 loaded images (for debugging)

    im_number : int
        index of image to use for choosing the fiducial. Useful if the first
        few images do not show the fiducial fully
    plot_fiducials : bool
        Switch to control whether an overview of fiducials will be plotted

    fid_num_to_plot: int
        How many fiducials to plot (will be spread out over all images)

    per_row : int
        How many subplots displayed per row

    Returns
    -------

    A list containing the horizontal distance (in units of pix_width)
    between the two selected fiducial marks on each image.
    """

    # noinspection PyArgumentList
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)

    # noinspection PyGlobalUndefined
    global drawing, ix, iy, x1, x2, y1, y2

    # Save interactive state, and set to non-interactive
    interactive_state = plt.isinteractive()
    matplotlib.interactive(False)

    # Variables for GUI interaction:
    drawing = False  # true if mouse is pressed
    ix, iy, x1, y1, x2, y2 = -1, -1, 0, 0, 0, 0

    # mouse callback function for drawing rectangle on image
    # noinspection PyShadowingNames,PyUnusedLocal,PyIncorrectDocstring
    def on_mouse(event, x, y, flags, param):
        """
        Callback function for use with an OpenCV window that draws a rectangle

        Parameters
        ----------
        event : OpenCV event
            event that is passed by OpenCV window
        x :
            x position of mouse cursor
        y :
            y position of mouse cursor
        param : list
            list of parameters used in the functions
            [im1, im2]
        """

        global ix, iy, drawing, x1, x2, y1, y2

        if event is cv2.EVENT_LBUTTONDOWN:
            drawing = True

            # every time left button is down, clear
            #   img1[:] =     img2[:]
            param[0][:] = param[1][:]
            ix, iy = x, y
            x1, y1 = max(x, 0), max(y, 0)

        elif event is cv2.EVENT_MOUSEMOVE:
            if drawing is True:
                # img values become img2 values
                #   img1[:] =     img2[:]
                param[0][:] = param[1][:]
                cv2.rectangle(param[0], (ix, iy), (x, y), (0, 255, 255), 1)

        elif event is cv2.EVENT_LBUTTONUP:
            drawing = False
            x2, y2 = max(x, 0), max(y, 0)
            cv2.rectangle(param[0], (ix, iy), (x, y), (0, 255, 255), 1)

    # ##################################
    # Reading the images into memory. #
    ###################################
    if im_list is None:
        im_list = readimages()

    print("Pixel width is " + repr(pix_width) + "m\n")

    #######################################################
    # Crop image so we don't have to process as much data #
    #######################################################
    # Information popup
    popup = QtGui.QMessageBox()
    popup.setText("In the following dialog, please select a reduced "
                  "area where the fiducials are expected to be found.")
    popup.setWindowTitle("Cropping images")
    popup.setWindowFlags(popup.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    popup.exec_()

    # Select crop area from first image
    img = cv2.cvtColor(im_list[0].copy(), cv2.COLOR_GRAY2RGB)
    img2 = img.copy()
    img3 = img.copy()

    cropwinname = 'Select rectangle for subregion (enter to submit)'
    cv2.namedWindow(cropwinname, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(cropwinname, on_mouse, param=[img, img2, img3])
    while True:
        cv2.imshow(cropwinname, img)
        k = cv2.waitKey(1) & 0xFF
        if k is 13:  # enter key
            cv2.destroyAllWindows()
            break
        elif k is 27:
            cv2.destroyAllWindows()
            print("No crop area selected, using full region")
            break
    print("Box coordinates are(x1, y1), "
          "(x2, y2): ({}, {}), ({}, {})".format(x1, y1, x2, y2))

    # If there is a selected window, crop images:
    if x1 is not 0 and x2 is not 0:
        # Crop each image (in a loop so we can track progress)
        im_list_cropped = [0] * len(im_list)
        for i, x in enumerate(tqdm(im_list, desc='Cropping images')):
            im_list_cropped[i] = x[min(y1, y2):max(y1, y2),
                                   min(x1, x2):max(x1, x2)]

    # otherwise, use whole window:
    else:
        im_list_cropped = im_list

    ####################################
    # Select fiducial marks from image #
    ####################################
    # Information popup
    popup = QtGui.QMessageBox()
    popup.setText("In the following two dialogs, please select one rectangle "
                  "to be used as a fiducial to track. Press enter after  "
                  "each selection.")
    popup.setWindowTitle("Selecting fiducials")
    popup.setWindowFlags(popup.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    popup.exec_()

    # Set template values from first (cropped) image
    img = cv2.cvtColor(im_list_cropped[im_number].copy(), cv2.COLOR_GRAY2RGB)
    img2 = img.copy()
    img3 = img.copy()

    # Getting fiducial locations from image
    winname1 = 'Select rectangle for fiducial 1 (enter to submit)'
    cv2.namedWindow(winname1)
    cv2.setMouseCallback(winname1, on_mouse, param=[img, img2, img3])
    # three copies of same image
    # Select fiducial 1 from first image
    while True:
        cv2.imshow(winname1, img)
        k = cv2.waitKey(1) & 0xFF
        if k is 13:  # enter key
            cv2.destroyAllWindows()
            break
        elif k is 27:
            cv2.destroyAllWindows()
            raise ValueError("Selection canceled")

    if x1 is 0:
        raise ValueError("No fiducial selected")
    template_left = cv2.cvtColor(img[min(y1, y2):max(y1, y2),
                                 min(x1, x2):max(x1, x2)],
                                 cv2.COLOR_RGB2GRAY)

    # Select fiducial 2 from second image
    img = cv2.cvtColor(im_list_cropped[im_number].copy(), cv2.COLOR_GRAY2RGB)
    winname2 = 'Select rectangle for fiducial 2 (enter to submit)'
    cv2.namedWindow(winname2)
    cv2.setMouseCallback(winname2, on_mouse, param=[img, img2, img3])
    while True:
        cv2.imshow(winname2, img)
        k = cv2.waitKey(1) & 0xFF
        if k is 13:  # enter key
            cv2.destroyAllWindows()
            break
        elif k is 27:
            cv2.destroyAllWindows()
            raise ValueError("No fiducial selected")
    template_right = cv2.cvtColor(img[min(y1, y2):max(y1, y2),
                                  min(x1, x2):max(x1, x2)],
                                  cv2.COLOR_RGB2GRAY)

    width_pix = [0] * len(im_list)

    w_l, h_l = template_left.shape[::-1]
    w_r, h_r = template_right.shape[::-1]

    #################################
    # Track fiducials in each image #
    #################################
    # If plotting the fiducials is requested, figure out proper shape
    # for subplot array
    if plot_fiducials:
        # rows is one larger than the number that we need to plot
        # (unless square array)
        rows = int(np.ceil(float(fid_num_to_plot) / per_row))

        # create left and right figures/subplot axes
        left_f, left_axarr = plt.subplots(nrows=rows, ncols=per_row)
        right_f, right_axarr = plt.subplots(nrows=rows, ncols=per_row)

        # generate list of images for which to plot by converting an evenly
        # spaced range to ints
        to_plot = [int(round(x)) for x in
                   np.linspace(0, len(im_list) - 1, fid_num_to_plot)]

        # initialize subplot counter j
        j = 0

    # Use TM_CCOEFF_NORMED method for fiducial finding
    def get_match_coordinates(image,
                              template,
                              w,
                              h,
                              match_method='cv2.TM_CCOEFF_NORMED',
                              check_dup=False,
                              dup_coord=None,
                              dup_thresh=30):
        """
        Get coordinates of template within image. If desired, will check if
        coordinates found are close to those given, in which case the second
        best match will be returned. Helps prevent finding the same fiducial
        mark twice.

        Parameters
        ----------
        image : OpenCV image
            image in which to find the fiducial
        template : OpenCV image
            fiducial (template image) to find
        w : int
            width of fiducial (in pixels)
        h : int
            height of fiducial (in pixels)
        match_method : string
            method to use with OpenCV matchTemplate. The default usually
            works well
        check_dup : bool
            switch controls whether or not to check if this fiducial is the
            same as another that has already been found
        dup_coord : tuple
            coordinates (in numpy order) of a previously found fiducial
        dup_thresh : int
            the number of pixels required between fiducials

        Returns
        -------
        y_1, x_1, y_2, x_2 : int
            y, x coordinates of top left (1) and bottom right (2) extents of
            the area in the image that matches the fiducial, respectively

        match_center : tuple
            coordinates in numpy (y, x) order of the center of the fiducial
            match location within the image (used for calculating distance
            between the fiducials)
        """
        # Apply template matching for  fiducial
        res = cv2.matchTemplate(image, template, eval(match_method))

        # Find two best matches for the fiducial:
        coord = peak_local_max(res, min_distance=10, num_peaks=2)

        # top_l and bot_r are in (y,x) numpy order
        top_l = coord[0]
        bot_r = (top_l[0] + h,
                 top_l[1] + w)

        # match_center is center location of the fiducial
        match_center = (top_l[0] + h / 2,
                        top_l[1] + w / 2)

        # save boundary positions of fiducial
        y_1, x_1 = top_l
        y_2, x_2 = bot_r

        # If check_dup is specified, compare the distance between the
        # fiducial match and the given coordinates. If they are close,
        # return the second-best match, as it is likely the true fiducial
        if check_dup:
            # Calculate pixel distance between fiducial marks (x coordinates)
            w_pix = abs(match_center[1] - dup_coord[1])

            # If fiducials are close
            if w_pix < 30:
                # Use second match:
                top_l = coord[1]
                bot_r = (top_l[0] + h,
                         top_l[1] + w)

                # match_center is center of fiducial, in numpy order
                match_center = (top_l[0] + h / 2,
                                top_l[1] + w / 2)

        return y_1, x_1, y_2, x_2, match_center

    # Loop through cropped images to find fiducial locations
    for i, im in enumerate(tqdm(im_list_cropped, desc='Tracking fiducials')):

        # LEFT FIDUCIAL
        # noinspection PyTupleAssignmentBalance
        ly1, lx1, ly2, lx2, match_left_center = \
            get_match_coordinates(im, template_left, w_l, h_l)

        # RIGHT FIDUCIAL
        # noinspection PyTupleAssignmentBalance
        ry1, rx1, ry2, rx2, match_right_center = \
            get_match_coordinates(im, template_right, w_r, h_r,
                                  check_dup=True, dup_coord=match_left_center)

        if plot_fiducials:
            # Add plots for each fiducial
            if i in to_plot and j < fid_num_to_plot:
                left_axarr[j // per_row, j % per_row].set_title("L " + repr(i))
                left_axarr[j // per_row, j % per_row].imshow(
                    im[ly1:ly2, lx1:lx2], cmap='gray', interpolation='nearest')
                left_axarr[j // per_row, j % per_row].set_axis_off()

                right_axarr[j // per_row, j % per_row].set_title("R " +
                                                                 repr(i))
                right_axarr[j // per_row, j % per_row].imshow(
                    im[ry1:ry2, rx1:rx2], cmap='gray', interpolation='nearest')
                right_axarr[j // per_row, j % per_row].set_axis_off()

                j += 1

            if fid_num_to_plot <= j < per_row * rows:
                left_axarr[j // per_row, j % per_row].set_axis_off()
                right_axarr[j // per_row, j % per_row].set_axis_off()
                j += 1

        # Calculate pixel distance between fiducial marks (x coordinates)
        width_pix[i] = abs(match_right_center[1] - match_left_center[1])

    if plot_fiducials:
        left_f.suptitle('Left fiducial')
        right_f.suptitle('Right fiducial')

        left_f.show()
        left_f.canvas.set_window_title('Left fiducials')

        right_f.show()
        right_f.canvas.set_window_title('Right fiducials')

    # Convert from pixels to meters:
    width_m = [x * pix_width for x in width_pix]

    matplotlib.interactive(interactive_state)

    return width_m


# noinspection PyTypeChecker
def _convert_units(to_convert,
                   input_u,
                   output_u,
                   ):
    """
    Convert values in a list from input_u to output_u

    Parameters
    ----------
    to_convert: list or numeric
        values to convert from one unit to another
    input_u: str
        ['m', 'cm', 'mm', 'um', or 'nm']
    output_u: str
        ['m', 'cm', 'mm', 'um', or 'nm']

    Returns
    -------
    list
        values in new units
    """
    factors = {'m': 1e0, 'cm': 1e2, 'mm': 1e3, 'um': 1e6, 'nm': 1e9}

    if input_u not in factors:
        raise ValueError(
            "Input unit not recognized. Possible values are [\'m\', \'cm\',"
            "\'mm\', \'um\', \'nm\']")
    if output_u not in factors:
        raise ValueError(
            "Output unit not recognized. Possible values are [\'m\', \'cm\',"
            "\'mm\', \'um\', \'nm\']")

    factor = factors[output_u] / factors[input_u]

    if isinstance(to_convert, list):
        return [i * factor for i in to_convert]

    else:
        return to_convert * factor


# noinspection PyTypeChecker
def plot_fid_distances(fid_distances,
                       input_units='m',
                       output_units='um',
                       slice_number_start=1,
                       plot_diff=False,
                       sns_style='white',
                       sns_context='poster',
                       sns_cmap=None,
                       sns_main_color=0,
                       sns_diff_color=0,
                       sns_kw=None,
                       ):
    """
    Plot a list of values as the distance between two fiducial markers

    Parameters
    ----------
    fid_distances: list
        Values to plot
    input_units: str
        units of values as provided
    output_units: str
        desired output units for plot
    slice_number_start: int
        starting slice number (for display purposes only)
    plot_diff: bool
        Switch to control whether or not a plot of the difference between
        subsequent slices is shown as well (as subplot)
    sns_style: str
        default style for seaborn ('white', 'dark', 'darkgrid', etc.)
    sns_context: str
        context for plotting with seaborn
    sns_cmap: list, str, tuple
        colormap for use with seaborn
        default is ["4C72B1","#004040","#023FA5","#8E063B","#098C09","#EF9708"]
        (light blue, dark teal, blue, red, green, orange)
        If str or tuple, then these parameters are passed to the
        seaborn.color_palette() function
    sns_main_color: int
        color (# from cmap) to use for plotting the fiducial distance
    sns_diff_color: int
        color (# from cmap) to use for plotting the differential distance
    sns_kw: dict
        additional arguments to be passed to seaborn.set_style
        (see http://goo.gl/WvLdc6 for details)

    Returns
    -------
    matplotlib figure, <matplotlib axes>
        Handle to figure that is plotted (and axes array if subplots)
    """
    # Default cmap and kw:
    if sns_kw is None:
        sns_kw = {}
    if sns_cmap is None:
        sns_cmap = ["#4C72B1", "#004040", "#023FA5", "#8E063B", "#098C09",
                    "#EF9708"]

    # Import and setup seaborn styles
    import seaborn as sns
    matplotlib.rcParams['mathtext.fontset'] = 'stixsans'
    sns.set_style(sns_style, sns_kw)
    sns.set_context(sns_context)
    if type(sns_cmap) is tuple:
        palette = sns.color_palette(*sns_cmap)
    else:
        palette = sns.color_palette(sns_cmap)
    sns.color_palette(palette)

    # convert fid_distances to proper output units (raises ValueError if bogus
    # units)
    fid_distances = _convert_units(fid_distances, input_units, output_units)

    # set up list of slice numbers to display
    slice_numbers = range(slice_number_start,
                          len(fid_distances) + slice_number_start)

    if output_units is 'um':
        output_units = "\mu m"

    if not plot_diff:
        fig = plt.figure()
        plt.plot(slice_numbers, fid_distances, color=palette[sns_main_color],
                 marker='.', linestyle=':')
        plt.xlabel("Image #")
        plt.ylabel("Distance between fiducials ($" + output_units + "$)")

        fig.suptitle('Distance between fiducials')

        fig.show()
        fig.canvas.set_window_title('Distance between fiducials')

        return fig
    else:
        fig, axarr = plt.subplots(nrows=2, ncols=1, sharex=True, squeeze=True)
        axarr[0].plot(slice_numbers, fid_distances,
                      color=palette[sns_main_color])
        axarr[1].plot(slice_numbers[1:], np.diff(fid_distances),
                      color=palette[sns_diff_color])

        axarr[1].set_xlabel("Image #")
        axarr[0].set_ylabel(
            "Distance between fiducials ($" + output_units + "$)")
        axarr[1].set_ylabel(
            "Deriv. dist. between fiducials ($" + output_units + "$)")
        return fig, axarr


def fit_fid_distances(fid_distances,
                      start_image=0,
                      end_image=None,
                      input_units='m',
                      output_units='nm',
                      fid_line_angle=40,
                      plot_results=True,
                      print_output=True,
                      reject_m=None
                      ):
    """
    Perform linear fit on widths between fiducials to get an average global
    slice thickness value.

    Parameters
    ----------
    fid_distances: list
        List of fiducial distances between slices in `input_units`
    start_image: int
        Which image to start the fit at (can exclude first `start_image`
        images if desired)
    end_image: int or None
        Which image to end the fit at.
        If None, all images will be used
    input_units: str
        Units that `fid_distances` is provided in.
    output_units: str
        Desired output units for plot
    fid_line_angle: numeric
        Half-angle (in degrees) of fiducial line triangle (angle a, below)

        ..  image:: half_angle.png
            :width: 200 px

    plot_results: boolean
        Whether or not to plot the results visually
    print_output: boolean
        Whether or not to print the output to the terminal
    reject_m: None or float
        "m" value to be used in the helper reject_outliers() function. If
        None, no modification of the data will be performed

    Returns
    -------
    avg_t: float
        Average thickness of slices, determined from fit
    """

    def reject_outliers(data, m=reject_m):
        """
        Helper function to remove outliers from data
        (from: http://stackoverflow.com/questions/11686720/
                is-there-a-numpy-builtin-to-reject-outliers-from-a-list)
        """
        if m is None:
            return data
        data = np.array(data)
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d / mdev if mdev else 0.

        return data[s < m]

    if end_image is None:
        # noinspection PyTypeChecker
        end_image = len(fid_distances) - 1

    y_val = reject_outliers(fid_distances[start_image:end_image])
    x_val = np.arange(start_image, start_image + len(y_val))

    fit = np.polyfit(x_val, y_val, deg=1)

    delta_x = _convert_units(fit[0], input_units, output_units)
    offset = _convert_units(fit[1], input_units, output_units)
    # noinspection PyTypeChecker
    delta_t = delta_x / (2 * np.tan(np.radians(fid_line_angle)))

    if print_output:
        print('Average fiducial delta_x is %.2f nm' % delta_x)
        print('Fiducial delta_x offset is %.2f nm' % offset)
        print('Average slice thickness is %.2f nm' % -delta_t)

    if plot_results:
        plot_fid_distances(fid_distances[:end_image])
        x = np.arange(0, end_image)
        y = _convert_units(offset, output_units, 'um') + _convert_units(
            delta_x, output_units, 'um') * x
        ax = plt.gca()
        f = plt.gcf()
        plt.plot(x, y, lw=1, c='k', ls='--')
        plt.text(0.54, 0.9, 'Avg. distance = %.2f nm' % delta_x, fontsize=25,
                 transform=ax.transAxes)
        plt.text(0.458, 0.85, 'Avg. slice thickness = %.2f nm' % -delta_t,
                 fontsize=25, transform=ax.transAxes)

        f.suptitle('Fitted fiducial distances')
        f.show()
        f.canvas.set_window_title('Fitted distance between fiducials')


def image_browser(im_list=None,
                  downsize=False,
                  downsizefactor=0.5,
                  labelimages=False,
                  ):
    """
    Open an OpenCV window that can browse through images using simple keyboard
    controls

    Parameters
    ----------
    im_list: list
        List of OpenCV images that will be navigated. If None, a Qt dialogue
        is opened to select a directory from which to read .tif files
    downsize: bool
        Switch to control whether images are downsized when reading into
        memory (for easier visualization)
    downsizefactor: float
        Factor by which to downsize the images (0.5 will make each dimension
        half it's original size)
    labelimages: bool
        Switch to control whether or not a text label will be written on the
        image to show it's position in the stack. Note, this is
        written onto the image itself, and will persist for future
        operations on the image list, so this option should not be used if
        this image list is to be used otherwise.

    Notes
    -----
    The player is controlled with keyboard shortcuts:

    =========       =========
    Shortcut        Action
    =========       =========
    ``f``           Animate stack forward
    ``d``           Animate stack backward
    ``s``           Stop animation
    ``+``           Double the speed of animation (faster)
    ``-``           Half the speed of animation (slower)
    ``n``           Step forwards by one image
    ``b``           Step backwards by one image
    ``Esc``         Exit the image browser
    =========       =========
    """

    # If im_list isn't given, read it from a qt dialogue
    if im_list is None:
        im_list = readimages()

    # Downsize the images (if requested)
    if downsize:
        im_list_small = [
            cv2.resize(i, (0, 0), fx=downsizefactor, fy=downsizefactor) for i
            in im_list]
    else:
        im_list_small = im_list

    i = 0
    speed = 50  # initial speed for playing the image through

    imgs = im_list_small

    # create named OpenCV window
    instructions = 'n: next, b: previous, f: play forward, ' \
                   'd: play backward, s: stop, esc: exit, ' \
                   '-: slow down, ' \
                   '+: speed up'
    cv2.namedWindow(instructions, cv2.WINDOW_AUTOSIZE)

    # If requested, label each image with a text annotation
    if labelimages:
        for i, im in enumerate(im_list):
            cv2.putText(imgs[i], repr(i + 1) + "/" + repr(len(im_list)),
                        (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
        i = 0

    # infinite loop provides an image browser
    while True:
        moveon = False  # switch that says we should run the loop again
        playfwd = False  # switch that says we're playing forwards
        playbkwd = False  # switch that says we're playing backwards
        noplay = True  # switch that says we're not playing
        while not moveon:
            if i >= len(im_list):
                i = len(im_list) - 1
            elif i < 0:
                i = 0

            if playfwd:
                i += 1
                if i >= len(im_list):
                    i = len(im_list) - 1
                    playfwd = False
                    noplay = True
                else:
                    noplay = False
                cv2.imshow(instructions, imgs[i])
                k = cv2.waitKey(int(speed))
                if k is 27:
                    cv2.destroyWindow(instructions)
                    return None
                elif k is ord('s'):
                    playfwd = False
                    noplay = True
                elif k is ord('d'):
                    playfwd = False
                    playbkwd = True
                elif k is 45:  # slow down
                    speed *= 2
                elif k is 43:  # speed up
                    speed //= 2  # integer division
                    if speed is 0:
                        speed = 1

            if playbkwd:
                i -= 1
                if i < 0:
                    i = 0
                    playbkwd = False
                    noplay = True
                else:
                    noplay = False
                cv2.imshow(instructions, imgs[i])
                k = cv2.waitKey(int(speed))
                if k is 27:
                    cv2.destroyWindow(instructions)
                    return None
                elif k is ord('s'):
                    playbkwd = False
                    noplay = True
                elif k is ord('f'):
                    playbkwd = False
                    playfwd = True
                elif k is 45:  # slow down
                    speed *= 2
                elif k is 43:  # speed up
                    speed //= 2  # integer division
                    if speed is 0:
                        speed = 1

            if noplay:
                cv2.imshow(instructions, imgs[i])
                k = cv2.waitKey(0)
                if k is 27:
                    cv2.destroyWindow(instructions)
                    return None
                elif k is ord('b'):
                    moveon = True
                    i -= 1
                elif k is ord('n'):
                    moveon = True
                    i += 1
                elif k is ord('f'):
                    playfwd = True
                elif k is ord('d'):
                    playbkwd = True
                elif k is 45:  # slow down
                    speed *= 2
                elif k is 43:  # speed up
                    speed //= 2  # integer division
                    if speed is 0:
                        speed = 1
                else:
                    pass


def export_video(im_list=None,
                 filename=None,
                 fourcc=None,
                 fps=20,
                 downsize=False,
                 downsizefactor=0.5,
                 labelimages=False,
                 labelsize=None):
    """
    Use OpenCV to write a video of all the images

    Parameters
    ----------

    im_list: list
        List of OpenCV images that will be navigated. If None, a Qt dialogue
        is opened to select a directory from which to read images
    filename: str
        Name of file to save as video
    fourcc: None or str
        Codec to use for writing video (see
        http://www.fourcc.org/codecs.php) supplied as four character string
        (such as 'DIVX'). If None, dialog will be presented to the user to
        choose.
    fps: int
        frames per second to use in output
    downsize: bool
        Switch to control whether images are downsized when reading into
        memory (for easier visualization)
    downsizefactor: float
        Factor by which to downsize the images (0.5 will make each dimension
        half it's original size)
    labelimages: bool
        Switch to control whether or not a text label will be written on the
        image to show it's position in the stack. Note, this is written onto
        the image itself, and will persist for future operations on the image
        list, so this option should not be used if this image list is to be
        used otherwise.
    labelsize: int
        factor to change how large the labels will be written. If None,
        an appropriate default size will be attempted

    Returns
    -------
    None
    """
    import platform
    import logging
    if platform.system() == 'Windows':
        logging.warning("Results of video export are hit-or-miss due "
                        "to poor codec support in Windows. Best guess, "
                        "try fourcc='MSVC' or select 'Microsoft Video' in "
                        "the pop-up window to get a useful result.")

    # If im_list isn't given, read it from a qt dialogue
    if im_list is None:
        im_list = readimages()

    # Downsize the images (if requested)
    if downsize:
        im_list_small = [
            cv2.resize(i, (0, 0), fx=downsizefactor, fy=downsizefactor) for i
            in im_list]
    else:
        im_list_small = im_list

    # Get size of image:
    height, width = im_list_small[0].shape

    # Get number of digits in image list length:
    order = str(len(str(len(im_list_small))))

    # Try to auto-choose label size and label thickness/position:
    if labelsize is None:
        labelsize = width / 500
    border_thick = labelsize * 3
    text_thick = labelsize
    text_y = labelsize * 40

    # Label images:
    if labelimages:
        for i, im in enumerate(im_list_small):
            cv2.putText(im_list_small[i],
                        str("{:0" + order + "}").format(i + 1) +
                        "/" + repr(len(im_list_small)), (20, text_y),
                        cv2.FONT_HERSHEY_DUPLEX, labelsize, (255, 255, 255),
                        border_thick, 8)
            cv2.putText(im_list_small[i],
                        str("{:0" + order + "}").format(i + 1) +
                        "/" + repr(len(im_list_small)), (20, text_y),
                        cv2.FONT_HERSHEY_DUPLEX, labelsize, (0, 255, 255),
                        text_thick, 8)

    # Determine write integer value to use for codec
    if fourcc is None:
        fourcc_int = -1
    else:
        # noinspection PyArgumentList
        fourcc_int = cv2.VideoWriter_fourcc(*fourcc)

    # Create the VideoWriter object
    video = cv2.VideoWriter(filename,
                            fourcc_int,
                            fps,
                            (width, height))

    # Write the actual video
    for i in tqdm(im_list_small, desc='Writing video'):
        video.write(i)
    cv2.destroyAllWindows()
    video.release()

    print("\nTo convert to a more suitable file size (and better format), "
          "now use ffmpeg on the output. \n\nSomething like:")
    print("%%bash\n"
          "ffmpeg -i {}  -f mp4 -vcodec libx264 -preset slow -crf 29  "
          "-y {}.mp4".format(filename, filename[:-4]))


# noinspection PyTypeChecker
def slice_thickness(fid_distances,
                    fid_line_angle=40,
                    input_units='m',
                    output_units='nm',
                    ):
    """
    Calculate the thickness of a series of slices from the fiducial widths

    Parameters
    ----------

    fid_distances: list
        list of distance between fiducials (calculated from trackfiducials() )
    fid_line_angle: float
        half-angle (in degrees) of fiducial line triangle (angle a, below)

        ..  image:: half_angle.png
            :width: 200 px

    input_units: str
        unit of input values (must be one of those supported by _convert_units
    output_units: str
        desired unit of output (must be one of those supported by
        _convert_units


    Returns
    -------
    thickness: list
        list of floats giving the difference of each slice
    mean: float
        mean thickness value
    std: float
        std dev of thickness values
    """

    # Convert lengths to desired units
    fid_distances = _convert_units(fid_distances, input_units, output_units)

    thickness = [x / (2 * np.tan(np.radians(fid_line_angle))) for x in
                 np.diff(fid_distances)]

    mean = np.mean(thickness)
    std = np.std(thickness)

    return [-1 * x for x in thickness], mean, std


def plot_thicknesses(thicknesses,
                     lowess_factor=0.05,
                     axes_limits='auto',
                     units='nm',
                     xlabel='Slice #',
                     ylabel='auto',
                     plot_data=True,
                     dataplotkw=None,
                     plot_lowess=True,
                     lowessplotkw=None,
                     plot_mean=True,
                     meanplotkw=None,
                     plot_std=True,
                     stdplotkw=None,
                     plot_legend=True,
                     legend_loc='best',
                     sns_style='white',
                     sns_context='poster',
                     sns_cmap=None,
                     sns_color_data=1,
                     sns_color_lowess=2,
                     sns_color_mean=3,
                     sns_color_std=4,
                     sns_style_kw=None,
                     ):
    """
    Plots a visualization of slice thickness measurements, as well as
    descriptive data

    Parameters
    ----------
    thicknesses: list
        thickness data to be plotted
    lowess_factor: float
        factor to be used when smoothing thickness data for plotting (valid
        values are [0-1]) the higher the factor used, the more smoothed the
        data will be
    axes_limits: 'auto' or list of int
        axes limits to use when displaying the data. If 'auto', the limits
        will be determined from the data; otherwise, should be given in the
        order [xmin, xmax, ymin, ymax]
    units: str
        units that values are given in (default of 'nm')
    xlabel: str
        label to use for the x-axis
    ylabel: str
        label to use for the y-axis
        if 'auto', label will be built including the units
    plot_data: bool
        Switch to control whether or not raw data is plotted
    dataplotkw: dict or None
        dictionary containing additional keyword arguments for the data
        scatterplot default included parameters are marker, linewidths,
        and label, which are set in the code if the value is None
    plot_lowess: bool
        Switch to control whether or not smoothed data is plotted
    lowessplotkw: dict or None
        dictionary containing additional keyword arguments for the LOWESS
        regression line plot default included parameters are linewidth.
        label is defined in the code (if not given here)
        defaults are set in the code if the value is None
    plot_mean: bool
        Switch to control whether or not data mean is plotted
    meanplotkw: dict or None
        dictionary containing additional keyword arguments for the mean line
        plot default included parameters are lw. label is defined in the
        code (if not given here) defaults are set in the code if the value
        is None
    plot_std: bool
        Switch to control whether or not data std dev is plotted
    meanplotkw: dict or None
        dictionary containing additional keyword arguments for the std dev
        line plots default included parameters are lw and ls. label is
        defined in the code (if not given here) defaults are set in the code
        if the value is None
    plot_legend: bool
        Switch to control whether or not legend is shown on the plot
    legend_loc: str or int
        see http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
        for details
        Desired position for the legend
    sns_style: str
        default style for seaborn ('white', 'dark', 'darkgrid', 'whitegrid')
    sns_context: str
        context for plotting with seaborn
    sns_cmap: list, str, tuple, or None
        colormap for use with seaborn
        default is ["4C72B1","#004040","#023FA5","#8E063B","#098C09","#EF9708"]
        (light blue, dark teal, blue, red, green, orange)
        If str or tuple, then these parameters are passed to the
        seaborn.color_palette() function
        default cmap is set in the code if the value is None
    sns_color_data: int
        color (# from cmap) to use for plotting the thickness data
    sns_color_lowess: int
        color (# from cmap) to use for plotting the lowess-smoothed data
    sns_color_mean: int
        color (# from cmap) to use for plotting the data mean
    sns_color_std: int
        color (# from cmap) to use for plotting the data std
    sns_style_kw: dict or None
        additional arguments to be passed to seaborn.set_style
        defaults are set in the code if the value is None
        (see http://goo.gl/WvLdc6 for details)

    Returns
    -------
    fig = Handle to figure that is plotted
    """
    import statsmodels.api as sm
    matplotlib.rcParams['mathtext.fontset'] = 'stixsans'

    # Checks on axes_limits parameter:
    if axes_limits is 'auto':
        pass
    elif len(axes_limits) is not 4:
        print("Specified axes_limits should be length 4. Resetting to "
              "\'auto\'.")
        axes_limits = 'auto'
    elif type(axes_limits) is not list:
        print("Specified axes_limits should be a list or \'auto\'. "
              "Resetting to \'auto\'.")
        axes_limits = 'auto'
    elif not all([isinstance(x, (int, float)) for x in axes_limits]):
        print("Specified axes_limits should be a list of numbers of length "
              "4. Resetting to \'auto\'.")
        axes_limits = 'auto'

    # Defaults for mutable type arguments
    if dataplotkw is None:
        dataplotkw = {'s': 40, 'marker': 'o', 'linewidths': 0.3,
                      'label': 'Measured slice thickness'}
    if lowessplotkw is None:
        lowessplotkw = {'linewidth': 2}
    if meanplotkw is None:
        meanplotkw = {'lw': 2}
    if stdplotkw is None:
        stdplotkw = {'lw': 2, 'ls': 'dashed'}
    if sns_cmap is None:
        sns_cmap = ["#4C72B1", "#004040", "#023FA5", "#8E063B", "#098C09",
                    "#EF9708"]
    if sns_style_kw is None:
        sns_style_kw = {'legend.frameon': True}

    # Import and setup seaborn styles
    import seaborn as sns
    matplotlib.rcParams['mathtext.fontset'] = 'stixsans'
    sns.set_style(sns_style, sns_style_kw)
    sns.set_context(sns_context)
    if type(sns_cmap) is tuple:
        palette = sns.color_palette(*sns_cmap)
    else:
        palette = sns.color_palette(sns_cmap)
    sns.color_palette(palette)

    fig = plt.figure()

    x = range(len(thicknesses))  # range (x values) for the slice numbers
    y = thicknesses  # actual measured thickness data
    i = lowess_factor  # factor by which to smooth the data

    if plot_data:
        if 'label' not in dataplotkw:
            dataplotkw['label'] = 'Measured slice thickness'
        plt.scatter(x, y, c=palette[sns_color_data], **dataplotkw)
    if plot_lowess:
        lowess = sm.nonparametric.lowess(y, x, frac=i)
        if 'label' in lowessplotkw:
            print(lowessplotkw['label'])
        if 'label' not in lowessplotkw:
            lowessplotkw['label'] = 'LOWESS regression ($f={0:.2f}$)'.format(i)
        plt.plot(lowess[:, 0], lowess[:, 1], color=palette[sns_color_lowess],
                 **lowessplotkw)
    if plot_mean or plot_std:
        thick_mean = np.mean(thicknesses)
        thick_std = np.std(thicknesses)
    if plot_mean:
        if 'label' not in meanplotkw:
            meanplotkw['label'] = '$\mu = {0:.2f}$ ({1})'.format(thick_mean,
                                                                 units)
        plt.axhline(thick_mean, color=palette[sns_color_mean], **meanplotkw)
    if plot_std:
        if 'label' not in stdplotkw:
            stdplotkw['label'] = '$\mu \pm \sigma = ({0:.2f}, {1:.2f})$ ({' \
                                 '2})'. format(thick_mean - thick_std,
                                               thick_mean + thick_std,
                                               units)
        plt.axhline(thick_mean - thick_std, color=palette[sns_color_std],
                    **stdplotkw)
        del stdplotkw['label']
        plt.axhline(thick_mean + thick_std, color=palette[sns_color_std],
                    **stdplotkw)

    if plot_legend:
        plt.legend(loc=legend_loc)

    if ylabel is 'auto':
        ylabel = 'Measured slice thickness (' + units + ')'
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    # Set limits of axes
    if axes_limits is 'auto':
        plt.axis([0, len(x), -5, 1.2 * np.max(y)])
    else:
        plt.axis(axes_limits)

    return fig


def save_output(data,
                fname='slice_thicknesses_fibtracking.csv',
                overwrite=False,
                collabels='auto',
                units='m',
                delimiter=',',
                print_time_stamp=True,
                ):
    """
    Write the output contained in a list to a csv file

    Parameters
    ----------
    data: list
        list containing values to save (usually slice thicknesses)
    fname: str
        string containing name of file to which to write
    overwrite: bool
        if fname exists, switch to control whether to overwrite
    collabels: list, 'auto', or None
        labels to write as column headers. If 'auto', default of "Slice,
        Thickness (units)" will be used. If a list, use str values
        separated by commas.
    units: str
        units to write in output
    delimiter: str
        delimiter to use in output
    print_time_stamp: bool
        switch to control whether a time stamp is printed on the first line
        of the file
    Returns:
        None
    """
    import csv
    import time
    import datetime
    import os.path

    if os.path.exists(fname) and not overwrite:
        raise IOError(
            "File exists, please choose different name or use "
            "\'overwrite=True\'.")

    ts = datetime.datetime.fromtimestamp(time.time()).strftime(
        '%Y-%m-%d %H:%M:%S')

    if collabels is 'auto':
        collabels = ['Slice', 'Thickness (' + units + ')']
    elif type(collabels) is list:
        pass
    elif collabels is None:
        pass
    else:
        print("Did not understand column label input. Using default values.")
        collabels = ['Slice', 'Thickness (' + units + ')']

    with open(fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if print_time_stamp:
            csvfile.write(ts + '\n')

        if collabels:
            writer.writerow(collabels)

        for i, x in enumerate(data):
            writer.writerow([str(i), str(x)])

        print(ts)
        print("Wrote output to " + fname)


def import_csv_data(fname,
                    skip_rows=2,
                    delimiter=','):
    """
    Read a csv file (saved by `save_output`) and get data back in a format
    that can be used by the other methods in this module.

    Parameters
    ----------
    fname: str
        Filename to read from
    skip_rows: int
        Number of rows to skip at the beginning of the file (headers)
    delimiter: str
        Delimiter for csv file (usually ',')

    Returns
    -------
    data: NumPy array
        data from the requested file in the format expected by the other
        methods in this module
    """
    data = np.genfromtxt(fname,
                         skip_header=skip_rows,
                         delimiter=delimiter)[:, 1]
    return data


if __name__ == "__main__":
    trackfiducials(int(sys.argv[1]))
