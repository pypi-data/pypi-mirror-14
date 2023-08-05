.. |towrite| replace:: **to write** 


Package ``procgraph.components.debug_components``
------------------------------------------------------------

Components used for debugging and unit tests.

.. list-table::
   :widths: 30 70

   * - :ref:`* <block:*>`
     - Product of two signals.
   * - :ref:`+ <block:+>`
     - Sum of two signals.
   * - :ref:`- <block:->`
     - Implements the difference of two signals, taking care of overflows. 
   * - :ref:`/ <block:/>`
     - Ratio of two signals.
   * - :ref:`constant <block:constant>`
     - Output a numerical constant that never changes. 
   * - :ref:`gain <block:gain>`
     - A simple example of a gain block.
   * - :ref:`identity <block:identity>`
     - This block outputs the inputs, unchanged.
   * - :ref:`info <block:info>`
     - Prints more compact information about the inputs than :ref:`block:print`. 
   * - :ref:`print <block:print>`
     - Print a representation of the input values along with their timestamp.


Package ``procgraph_cv``
------------------------------------------------------------

Blocks using the OpenCV library.

.. list-table::
   :widths: 30 70

   * - :ref:`gradient <block:gradient>`
     - Computes the gradient of an image using a Sobel filter.
   * - :ref:`smooth <block:smooth>`
     - Smooths an image with a Gaussian filter.


Package ``procgraph_foo``
------------------------------------------------------------

An example package for ProcGraph that shows how to organize your code. 

.. list-table::
   :widths: 30 70

   * - :ref:`block_example <block:block_example>`
     - This is a documented example of the simplest block possible. 


Package ``procgraph_hdf``
------------------------------------------------------------

This is a set of blocks to read and write logs in HDF_ format. 

.. list-table::
   :widths: 30 70

   * - :ref:`hdfread <block:hdfread>`
     - This block reads a log written with :ref:`block:hdfwrite`.
   * - :ref:`hdfread_many <block:hdfread_many>`
     - This block is a variation on :ref:`block:hdfread` that can concatenate the output of logs stored in multiple HDF files. 
   * - :ref:`hdfread_many_test <block:hdfread_many_test>`
     - This is a simple test for :ref:`block:hdfread_many`.
   * - :ref:`hdfread_test <block:hdfread_test>`
     - This is a simple test that reading from HDF files is happening correctly.
   * - :ref:`hdfwrite <block:hdfwrite>`
     - This block writes the incoming signals to a file in HDF_ format. 


Package ``procgraph_images``
------------------------------------------------------------

Blocks for basic operations on images. 

.. list-table::
   :widths: 30 70

   * - :ref:`blend <block:blend>`
     - Blend two or more images. 
   * - :ref:`border <block:border>`
     - Adds a block around the input image.
   * - :ref:`compose <block:compose>`
     - Compose several images in the same canvas. You should probably use :ref:`block:grid` in many situations. 
   * - :ref:`crop <block:crop>`
     - Crops an image by the given values
   * - :ref:`files_from_dir <block:files_from_dir>`
     - This block reads the filenames from a directory according to a given regexp. 
   * - :ref:`gray2rgb <block:gray2rgb>`
     - Converts a H x W grayscale into a H x W x 3 RGB image by replicating the gray channel over R,G,B.
   * - :ref:`grid <block:grid>`
     - A block that creates a larger image by arranging them in a grid.
   * - :ref:`posneg <block:posneg>`
     - Converts a 2D float value to a RGB representation, where red is positive, blue is negative, white is zero.
   * - :ref:`posterize <block:posterize>`
     - Posterizes the given image with the specified number of levels.
   * - :ref:`reshape2d <block:reshape2d>`
     - Reshapes x into (?, width) if x is 1D. If width is not given, it is set to be the sqrt(size). 
   * - :ref:`rgb2gray <block:rgb2gray>`
     - Converts a HxWx3 RGB image into a HxW grayscale image by computing the luminance.
   * - :ref:`scale <block:scale>`
     - Provides a RGB representation of the values by interpolating the range [min(value),max(value)] into the colorspace [min_color, max_color].
   * - :ref:`skim_top <block:skim_top>`
     - Cuts off the top percentile of the array.
   * - :ref:`skim_top_and_bottom <block:skim_top_and_bottom>`
     - Cuts off the top and bottom percentile of the array.
   * - :ref:`solid <block:solid>`
     - |towrite|


Package ``procgraph_io_misc``
------------------------------------------------------------

Miscellaneous functions to be better organized.

.. list-table::
   :widths: 30 70

   * - :ref:`as_json <block:as_json>`
     - Converts the input into a JSON string. 
   * - :ref:`pickle <block:pickle>`
     - Dumps the input as a :py:mod:`pickle` file.
   * - :ref:`pickle_group <block:pickle_group>`
     - Dumps the input as a :py:mod:`pickle` file, in the form of a dictionary  signal name -> value.
   * - :ref:`pickle_load <block:pickle_load>`
     - Dumps the input as a :py:mod:`pickle` file.
   * - :ref:`to_file <block:to_file>`
     - Prints the input line by line to a given file.


Package ``procgraph_mpl``
------------------------------------------------------------

Blocks using Matplotlib to display data.

.. list-table::
   :widths: 30 70

   * - :ref:`plot <block:plot>`
     - Plots the inputs using matplotlib. 


Package ``procgraph_mplayer``
------------------------------------------------------------

Blocks for encoding/decoding video based on MPlayer.

.. list-table::
   :widths: 30 70

   * - :ref:`mencoder <block:mencoder>`
     - Encodes a video stream using ``mencoder``. 
   * - :ref:`mplayer <block:mplayer>`
     - Decodes a video stream.


Package ``procgraph_numpy_ops``
------------------------------------------------------------

Various operations wrapping numpy functions.

.. list-table::
   :widths: 30 70

   * - :ref:`abs <block:abs>`
     - Wrapper around :np:data:`numpy.absolute`.
   * - :ref:`arctan <block:arctan>`
     - Wrapper around :np:data:`numpy.arctan`.
   * - :ref:`array <block:array>`
     - Converts the value to a Numpy array.
   * - :ref:`astype <block:astype>`
     - Converts an array using the ``astype`` function.
   * - :ref:`deg2rad <block:deg2rad>`
     - Converts degrees to radians (wrapper around :np:data:`numpy.radians`.)
   * - :ref:`dstack <block:dstack>`
     - Wrapper around :np:data:`numpy.ma.dstack`.
   * - :ref:`fliplr <block:fliplr>`
     - Flips the array left/right (wrapper for :py:func:`numpy.fliplr`.)
   * - :ref:`flipud <block:flipud>`
     - Flips the array up/down (wrapper for :py:func:`numpy.flipud`.)
   * - :ref:`gradient1d <block:gradient1d>`
     - Computes the gradient of a 1D array.
   * - :ref:`hstack <block:hstack>`
     - Wrapper around :np:data:`numpy.ma.hstack`.
   * - :ref:`log <block:log>`
     - Wrapper around :np:data:`numpy.log`.
   * - :ref:`max <block:max>`
     - Maximum over **all** elements.
   * - :ref:`maximum <block:maximum>`
     - Limits the numpy array to the given threshold.
   * - :ref:`mean <block:mean>`
     - Wrapper around :np:data:`numpy.mean`.
   * - :ref:`minimum <block:minimum>`
     - Limits the numpy array to the given threshold.
   * - :ref:`norm <block:norm>`
     - Returns the norm of the vector.
   * - :ref:`normalize_Linf <block:normalize_Linf>`
     - Normalize a vector such that ``|x|_inf = max(abs(x))= 1``.
   * - :ref:`outer <block:outer>`
     - Outer product of two vectors. 
   * - :ref:`rad2deg <block:rad2deg>`
     - Converts radians to degrees (wrapper around :np:data:`numpy.degrees`.)
   * - :ref:`real <block:real>`
     - Wrapper around :np:data:`numpy.real`.
   * - :ref:`select <block:select>`
     - Selects some of the elements of ``x``.
   * - :ref:`sign <block:sign>`
     - Wrapper around :np:data:`numpy.sign`.
   * - :ref:`smooth1d <block:smooth1d>`
     - Smooth the data using a window with requested size. 
   * - :ref:`square <block:square>`
     - Wrapper around :np:data:`numpy.square`.
   * - :ref:`sum <block:sum>`
     - Sum over **all** elements.
   * - :ref:`take <block:take>`
     - |towrite|
   * - :ref:`vstack <block:vstack>`
     - Wrapper around :np:data:`numpy.ma.vstack`.


Package ``procgraph_pil``
------------------------------------------------------------

Blocks for image operations based on the PIL library

.. list-table::
   :widths: 30 70

   * - :ref:`imread <block:imread>`
     - Reads an image from a file.
   * - :ref:`imwrite <block:imwrite>`
     - Writes an image to a file.
   * - :ref:`resize <block:resize>`
     - Resizes an image. 
   * - :ref:`text <block:text>`
     - This block provides text overlays over an image. 


Package ``procgraph_robotics``
------------------------------------------------------------

Some functions specific to robotics applications. 

.. list-table::
   :widths: 30 70

   * - :ref:`laser_display <block:laser_display>`
     - Produces a plot of a range-finder scan. 
   * - :ref:`laser_dot_display <block:laser_dot_display>`
     - Produces a plot of a range-finder scan variation (derivative). 
   * - :ref:`organic_scale <block:organic_scale>`
     - A (almost failed!) attempt to scale a signal into [-1,1] according to the history. 
   * - :ref:`pose2commands <block:pose2commands>`
     - Computes the velocity commands from the odometry data.
   * - :ref:`pose2vel_ <block:pose2vel_>`
     - Block used by :ref:`block:pose2commands`.
   * - :ref:`skim <block:skim>`
     - Cuts off the top and bottom percentile of the array.


Package ``procgraph_ros``
------------------------------------------------------------

This is a set of blocks to read and write logs in ROS_ Bag format. 

.. list-table::
   :widths: 30 70

   * - :ref:`bagread <block:bagread>`
     - This block reads a bag file (ROS logging format).
   * - :ref:`bagread_test <block:bagread_test>`
     - Test of the bagread block.
   * - :ref:`bagwrite <block:bagwrite>`
     - This block writes the incoming signals to a ROS bag file. 
   * - :ref:`ros2python <block:ros2python>`
     - Converts a ROS message to a Python object.
   * - :ref:`ros_scan2python <block:ros_scan2python>`
     - |towrite|


Package ``procgraph_signals``
------------------------------------------------------------

Blocks performing operations with a dynamic nature. 

.. list-table::
   :widths: 30 70

   * - :ref:`any <block:any>`
     - Joins the stream of multiple signals onto one output signal.
   * - :ref:`async <block:async>`
     - |towrite|
   * - :ref:`derivative <block:derivative>`
     - Computes the derivative of a quantity with 3 taps  (``x[t+1] - x[t-1]``). See also :ref:`block:derivative2`.
   * - :ref:`derivative2 <block:derivative2>`
     - Computes the derivative of a quantity with 2 taps (``x[t+1] - x[t]``). See also :ref:`block:derivative`.
   * - :ref:`extract <block:extract>`
     - This block extracts some of the components of a vector. 
   * - :ref:`forward_difference <block:forward_difference>`
     - Computes ``x[t+1] - x[t-1]`` normalized with timestamp. 
   * - :ref:`fps_data_limit <block:fps_data_limit>`
     - This block limits the output update to a certain framerate.
   * - :ref:`fps_limit <block:fps_limit>`
     - This block limits the output update to a certain *realtime* framerate. 
   * - :ref:`fps_print <block:fps_print>`
     - Prints the fps count for the input signals.
   * - :ref:`history <block:history>`
     - This block collects the history of a quantity, and outputs two signals ``x`` and ``t``. See also :ref:`block:historyt` and :ref:`block:last_n_samples`.
   * - :ref:`historyt <block:historyt>`
     - This block collects the signals samples of a signals, and outputs *one* signal containing a tuple  ``(t,x)``. See also :ref:`block:last_n_samples` and :ref:`block:history`. 
   * - :ref:`join <block:join>`
     - This block joins multiple signals into one.
   * - :ref:`last_n_samples <block:last_n_samples>`
     - This block collects the last N samples of a signals, and outputs two signals ``x`` and ``t``. See also :ref:`block:historyt` and :ref:`block:history`.
   * - :ref:`low_pass <block:low_pass>`
     - Implements simple low-pass filtering. 
   * - :ref:`make_tuple <block:make_tuple>`
     - Creates a tuple out of the input signals values. 
   * - :ref:`sieve <block:sieve>`
     - This block decimates the data in time by transmitting only one in ``n`` updates.
   * - :ref:`slice <block:slice>`
     - Slices a signal by extracting from index ``start`` to index ``end`` (INCLUSIVE).
   * - :ref:`sync <block:sync>`
     - This block synchronizes a set of streams to the first stream (the master). 
   * - :ref:`two_step_difference <block:two_step_difference>`
     - Computes ``x[t+1] - x[t]`` normalized with timestamp.
   * - :ref:`wait <block:wait>`
     - This block waits a given number of updates before transmitting the output signal.


Package ``procgraph_statistics``
------------------------------------------------------------

Blocks for common statistical operations.

.. list-table::
   :widths: 30 70

   * - :ref:`cov2corr <block:cov2corr>`
     - Compute the correlation matrix from the covariance matrix. If zero_diagonal = True, the diagonal is set to 0 instead of 1.
   * - :ref:`covariance <block:covariance>`
     - Computes the covariance matrix of the input.
   * - :ref:`expectation <block:expectation>`
     - Computes the sample expectation of a signal.
   * - :ref:`maximum_over_time <block:maximum_over_time>`
     - Computes the minimum of a signal over time.
   * - :ref:`minimum_over_time <block:minimum_over_time>`
     - Computes the minimum of a signal over time.
   * - :ref:`normalize <block:normalize>`
     - Removes the mean from a signal.
   * - :ref:`soft_variance <block:soft_variance>`
     - Computes the element-wise "soft" variance (exp. of error abs. value)
   * - :ref:`variance <block:variance>`
     - Computes the element-wise variance.


Package ``procgraph_yaml``
------------------------------------------------------------

YAML conversions.

.. list-table::
   :widths: 30 70

   * - :ref:`yaml2object <block:yaml2object>`
     - |towrite|

.. _`module:procgraph.components.debug_components`:


.. rst-class:: procgraph:module

Package ``procgraph.components.debug_components``
============================================================



.. rst-class:: procgraph:desc

Components used for debugging and unit tests.

.. _`block:*`:


.. rst-class:: procgraph:block

Block ``*``
------------------------------------------------------------------
Product of two signals.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: First signal.

- ``y``: Second signal.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``product``: Product of the two signals.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/operations.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/operations.py>`_. 


.. _`block:+`:


.. rst-class:: procgraph:block

Block ``+``
------------------------------------------------------------------
Sum of two signals.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: First signal.

- ``y``: Second signal.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``sum``: Sum of the two signals.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/operations.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/operations.py>`_. 


.. _`block:-`:


.. rst-class:: procgraph:block

Block ``-``
------------------------------------------------------------------
Implements the difference of two signals, taking care of overflows. 

Because that is rarely the semantics you want to give them.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``safe`` (default: None): Whether to use safe promotions. If not specified, we will do it but warn once.

- ``cases`` (default: {'uint16': 'int32', 'uint8': 'int16', 'uint32': 'int64'}): Promotion rules


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: First signal

- ``y``: Second signal


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x_minus_y``: Result of x - y


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/operations.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/operations.py>`_. 


.. _`block:/`:


.. rst-class:: procgraph:block

Block ``/``
------------------------------------------------------------------
Ratio of two signals.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: First signal.

- ``y``: Second signal.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``ratio``: First signal divided by the second.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/operations.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/operations.py>`_. 


.. _`block:constant`:


.. rst-class:: procgraph:block

Block ``constant``
------------------------------------------------------------------
Output a numerical constant that never changes. 

Example: ::

    |constant value=42| -> ...


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: Constant value to output.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``constant``: The constant value.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/constant.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/constant.py>`_. 


.. _`block:gain`:


.. rst-class:: procgraph:block

Block ``gain``
------------------------------------------------------------------
A simple example of a gain block.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``k``: Multiplicative gain


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``in``: Input value


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``out``: Output multiplied by k.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/gain.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/gain.py>`_. 


.. _`block:identity`:


.. rst-class:: procgraph:block

Block ``identity``
------------------------------------------------------------------
This block outputs the inputs, unchanged.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Input signals. (variable number: n >= 1)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Output signals, equal to input. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/identity.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/identity.py>`_. 


.. _`block:info`:


.. rst-class:: procgraph:block

Block ``info``
------------------------------------------------------------------
Prints more compact information about the inputs than :ref:`block:print`. 

For numpy arrays it prints their shape and dtype
instead of their values.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to describe. (variable number: n >= 1)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/info.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/info.py>`_. 


.. _`block:print`:


.. rst-class:: procgraph:block

Block ``print``
------------------------------------------------------------------
Print a representation of the input values along with their timestamp.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to print. (variable number: n >= 1)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph/components/debug_components/printc.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph/components/debug_components/printc.py>`_. 


.. _`module:procgraph_cv`:


.. rst-class:: procgraph:module

Package ``procgraph_cv``
============================================================



.. rst-class:: procgraph:desc

Blocks using the OpenCV library.

.. _`block:gradient`:


.. rst-class:: procgraph:block

Block ``gradient``
------------------------------------------------------------------
Computes the gradient of an image using a Sobel filter.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``aperture_size`` (default: 3): Aperture of the Sobel filter (odd). (int,odd,>=1)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``grayscale``: A field to derive. (HxW array float)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``gx``: Gradient in the *x* direction. (array(HxW,float))

- ``gy``: Gradient in the *y* direction. (array(HxW,float))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_cv/opencv_utils.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_cv/opencv_utils.py>`_. 


.. _`block:smooth`:


.. rst-class:: procgraph:block

Block ``smooth``
------------------------------------------------------------------
Smooths an image with a Gaussian filter.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``gaussian_std`` (default: 5.0): Std-deviation of the Gaussian filter. (float,>0)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``grayscale``: A field to derive. (HxW array float)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``smoothed``: The smoothed image. (array(HxW,float))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_cv/opencv_utils.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_cv/opencv_utils.py>`_. 


.. _`module:procgraph_foo`:


.. rst-class:: procgraph:module

Package ``procgraph_foo``
============================================================



.. rst-class:: procgraph:desc

An example package for ProcGraph that shows how to organize your code. 


.. rst-class:: procgraph:desc_rest

This is the documentation string for the package. Like all docstrings,
it consists of a short summary (above) and a longer description (this.)

.. _`block:block_example`:


.. rst-class:: procgraph:block

Block ``block_example``
------------------------------------------------------------------
This is a documented example of the simplest block possible. 

This docstring will be included in the generated documentation.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``bias`` (default: 0): Bias for the accelerator.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``baz``: Measured baz in the particle accelerator.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``baz_compensated``: Compensated baz value according to calibration.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_foo/example0_simplest_block.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_foo/example0_simplest_block.py>`_. 


.. _`module:procgraph_hdf`:


.. rst-class:: procgraph:module

Package ``procgraph_hdf``
============================================================



.. rst-class:: procgraph:desc

This is a set of blocks to read and write logs in HDF_ format. 


.. rst-class:: procgraph:desc_rest

You need the pytables_ package to be installed.

.. _pytables: http://pytables.org

.. _HDF: http://en.wikipedia.org/wiki/Hierarchical_Data_Format

.. _`block:hdfread`:


.. rst-class:: procgraph:block

Block ``hdfread``
------------------------------------------------------------------
This block reads a log written with :ref:`block:hdfwrite`.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: HDF file to read

- ``signals`` (default: None): Which signals to output (and in what order). Should be a comma-separated list. If you do not specify it  will be all signals (TODO: in the original order).

- ``quiet`` (default: False): If true, disables advancements status messages.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The signals read from the log. (signals are defined at runtime)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_hdf/hdfread.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_hdf/hdfread.py>`_. 


.. _`block:hdfread_many`:


.. rst-class:: procgraph:block

Block ``hdfread_many``
------------------------------------------------------------------
This block is a variation on :ref:`block:hdfread` that can concatenate the output of logs stored in multiple HDF files. 

The files are specified using a wildcard: for example, ``dir/*.h5``.

A difference with :ref:`block:hdfread` is that all signals
must be specified explicitly (:ref:`block:hdfread` can guess); the
reason is that we want to avoid reading unrelated logs with different
signals.

We check that all files specified have all required signals.

The logfiles are read in the order compatible with their timestamp.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``files``: HDF files to read; you can use the wildcard ``*``.

- ``signals``: Which signals to output (and in what order). Should be a comma-separated list.

- ``quiet`` (default: False): If true, disables advancements status messages.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The signals read from the logs. (signals are defined at runtime)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_hdf/hdfread_many.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_hdf/hdfread_many.py>`_. 


.. _`block:hdfread_many_test`:


.. rst-class:: procgraph:block

Block ``hdfread_many_test``
------------------------------------------------------------------
This is a simple test for :ref:`block:hdfread_many`.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``files``: File pattern

- ``signals``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_hdf/models/hdfread_many_test.pg <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_hdf/models/hdfread_many_test.pg>`_. 


.. _`block:hdfread_test`:


.. rst-class:: procgraph:block

Block ``hdfread_test``
------------------------------------------------------------------
This is a simple test that reading from HDF files is happening correctly.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: input hdf file


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_hdf/models/hdfread_test.pg <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_hdf/models/hdfread_test.pg>`_. 


.. _`block:hdfwrite`:


.. rst-class:: procgraph:block

Block ``hdfwrite``
------------------------------------------------------------------
This block writes the incoming signals to a file in HDF_ format. 

The HDF format is organized as follows: ::

     /            (root)
     /procgraph             (group with name procgraph)
     /procgraph/signal1     (table)
     /procgraph/signal2     (table)
     ...

Each table has the following fields:

     time         (float64 timestamp)
     value        (the datatype of the signal)

If a signal changes datatype, then an error is thrown.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: HDF file to write

- ``compress`` (default: 1): Whether to compress the hdf table.

- ``complib`` (default: zlib): Compression library (zlib, bzip2, blosc, lzo).

- ``complevel`` (default: 9): Compression level (0-9)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to be written (variable number: n >= 1)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_hdf/hdfwrite.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_hdf/hdfwrite.py>`_. 


.. _`module:procgraph_images`:


.. rst-class:: procgraph:module

Package ``procgraph_images``
============================================================



.. rst-class:: procgraph:desc

Blocks for basic operations on images. 


.. rst-class:: procgraph:desc_rest

This package contains blocks that perform basic operations
on images. The library has no software dependency.

For more complex operations see also :ref:`module:procgraph_cv` and
:ref:`module:procgraph_pil`

**Example**

Convert a RGB image to grayscale, and back to a RGB image:::


    |input| -> |rgb2gray| -> |gray2rgb| -> |output|

.. _`block:blend`:


.. rst-class:: procgraph:block

Block ``blend``
------------------------------------------------------------------
Blend two or more images. 

RGB images are interpreted as having full alpha (opaque).
All images must have the same width and height.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- images to blend (variable number: n >= 2)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: The output is a RGB image (no alpha)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/blend.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/blend.py>`_. 


.. _`block:border`:


.. rst-class:: procgraph:block

Block ``border``
------------------------------------------------------------------
Adds a block around the input image.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``color`` (default: [0, 0, 0]): border color (0-1 rgb)

- ``left`` (default: 0): pixel length for left border

- ``right`` (default: 0): pixel length for right border

- ``top`` (default: 0): pixel length for top border

- ``bottom`` (default: 0): pixel length for bottom border


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: Input image.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: Image with borders added around.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/border.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/border.py>`_. 


.. _`block:compose`:


.. rst-class:: procgraph:block

Block ``compose``
------------------------------------------------------------------
Compose several images in the same canvas. You should probably use :ref:`block:grid` in many situations. 

Example configuration: ::

    compose.positions = {y: [0,0], ys: [320,20]}


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width``: Dimension in pixels.

- ``height``: Dimension in pixels.

- ``positions``: A structure giving the position of each signal in the canvas.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Images to compose. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``canvas``: RGB image


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/compose.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/compose.py>`_. 


.. _`block:crop`:


.. rst-class:: procgraph:block

Block ``crop``
------------------------------------------------------------------
Crops an image by the given values


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``top`` (default: 0): |towrite|

- ``right`` (default: 0): |towrite|

- ``left`` (default: 0): |towrite|

- ``bottom`` (default: 0): |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/crop.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/crop.py>`_. 


.. _`block:files_from_dir`:


.. rst-class:: procgraph:block

Block ``files_from_dir``
------------------------------------------------------------------
This block reads the filenames from a directory according to a given regexp. 

For now the timestamp starts from 0 and it is fixed.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``dir``: Directory containing the image files.

- ``regexp`` (default: (\w+)_(\d+)\.jpg): Regular expression for images.

- ``fps`` (default: 20.0): Fixed frame per second.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``filename``: Image filename


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/images_from_dir.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/images_from_dir.py>`_. 


.. _`block:gray2rgb`:


.. rst-class:: procgraph:block

Block ``gray2rgb``
------------------------------------------------------------------
Converts a H x W grayscale into a H x W x 3 RGB image by replicating the gray channel over R,G,B.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``gray``: grayscale (array(HxW,uint8),H>0,W>0)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: A RGB image in shades of gray. (array(HxWx3,uint8))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/filters.py>`_. 


.. _`block:grid`:


.. rst-class:: procgraph:block

Block ``grid``
------------------------------------------------------------------
A block that creates a larger image by arranging them in a grid.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``cols`` (default: None): Columns in the grid.

- ``bgcolor`` (default: [0, 0, 0]): Background color.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Images to arrange in a grid. (variable number: n >= 1)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``grid``: Images arranged in a grid.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/imggrid.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/imggrid.py>`_. 


.. _`block:posneg`:


.. rst-class:: procgraph:block

Block ``posneg``
------------------------------------------------------------------
Converts a 2D float value to a RGB representation, where red is positive, blue is negative, white is zero.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``max_value`` (default: None): Maximum of absolute value (if None, detect). (float,>0)

- ``nan_color`` (default: [0.5, 0.5, 0.5]): Color to give for regions of NaN and Inf. (color)

- ``skim`` (default: 0): Fraction to skim (in percent). (float,>0,<100)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: The field to represent. (array[HxW])


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``posneg``: A RGB image. (array[HxWx3](uint8))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/copied_from_reprep.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/copied_from_reprep.py>`_. 


.. _`block:posterize`:


.. rst-class:: procgraph:block

Block ``posterize``
------------------------------------------------------------------
Posterizes the given image with the specified number of levels.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``levels`` (default: 2): number of levels (int,>=2)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: RGB image (array(HxWx3,uint8),H>0,W>0)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: A RGB image with the specified number of levels. (array(HxWx3,uint8))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/posterize.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/posterize.py>`_. 


.. _`block:reshape2d`:


.. rst-class:: procgraph:block

Block ``reshape2d``
------------------------------------------------------------------
Reshapes x into (?, width) if x is 1D. If width is not given, it is set to be the sqrt(size). 

If x is 2D, it is left alone.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width`` (default: None): |towrite|

- ``fill_value`` (default: nan): |towrite|

- ``height`` (default: None): |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/reshape_smart.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/reshape_smart.py>`_. 


.. _`block:rgb2gray`:


.. rst-class:: procgraph:block

Block ``rgb2gray``
------------------------------------------------------------------
Converts a HxWx3 RGB image into a HxW grayscale image by computing the luminance.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: RGB image (array(HxWx3,uint8),H>0,W>0)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: A RGB image in shades of gray. (array(HxW,uint8))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/filters.py>`_. 


.. _`block:scale`:


.. rst-class:: procgraph:block

Block ``scale``
------------------------------------------------------------------
Provides a RGB representation of the values by interpolating the range [min(value),max(value)] into the colorspace [min_color, max_color].


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``max_value`` (default: None): If specified, everything *above* is clipped. (float)

- ``nan_color`` (default: [1, 0, 0]): Color to give for regions of NaN and Inf. (color)

- ``min_value`` (default: None): If specified, everything *below* is clipped. (float)

- ``min_color`` (default: [1, 1, 1]): Color to give to the minimum values. (color)

- ``max_color`` (default: [0, 0, 0]): Color to give to the maximum values. (color)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: The field to represent. (array[HxW],H>0,W>0)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``scale``: A RGB image. (array[HxWx3](uint8))


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/copied_from_reprep.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/copied_from_reprep.py>`_. 


.. _`block:skim_top`:


.. rst-class:: procgraph:block

Block ``skim_top``
------------------------------------------------------------------
Cuts off the top percentile of the array.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``top_percent``: How much to cut off (decimal). (float,>=0,<90)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/copied_from_reprep.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/copied_from_reprep.py>`_. 


.. _`block:skim_top_and_bottom`:


.. rst-class:: procgraph:block

Block ``skim_top_and_bottom``
------------------------------------------------------------------
Cuts off the top and bottom percentile of the array.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``percent``: How much to cut off (decimal). (float,>=0,<90)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: Any numpy array. (array[x])


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: Skimmed version of ``a``. (array[x])


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/copied_from_reprep.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/copied_from_reprep.py>`_. 


.. _`block:solid`:


.. rst-class:: procgraph:block

Block ``solid``
------------------------------------------------------------------
|towrite|


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width``: |towrite|

- ``height``: |towrite|

- ``color``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_images/solid.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_images/solid.py>`_. 


.. _`module:procgraph_io_misc`:


.. rst-class:: procgraph:module

Package ``procgraph_io_misc``
============================================================



.. rst-class:: procgraph:desc

Miscellaneous functions to be better organized.

.. _`block:as_json`:


.. rst-class:: procgraph:block

Block ``as_json``
------------------------------------------------------------------
Converts the input into a JSON string. 

TODO: add example


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Inputs to transcribe as JSON. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``json``: JSON string.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_io_misc/json_misc.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_io_misc/json_misc.py>`_. 


.. _`block:pickle`:


.. rst-class:: procgraph:block

Block ``pickle``
------------------------------------------------------------------
Dumps the input as a :py:mod:`pickle` file.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: File to write to.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Anything pickable.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_io_misc/pickling.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_io_misc/pickling.py>`_. 


.. _`block:pickle_group`:


.. rst-class:: procgraph:block

Block ``pickle_group``
------------------------------------------------------------------
Dumps the input as a :py:mod:`pickle` file, in the form of a dictionary  signal name -> value.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: File to write to.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Any number of pickable signals. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_io_misc/pickling.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_io_misc/pickling.py>`_. 


.. _`block:pickle_load`:


.. rst-class:: procgraph:block

Block ``pickle_load``
------------------------------------------------------------------
Dumps the input as a :py:mod:`pickle` file.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: File to read from.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Object read from file


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_io_misc/pickling.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_io_misc/pickling.py>`_. 


.. _`block:to_file`:


.. rst-class:: procgraph:block

Block ``to_file``
------------------------------------------------------------------
Prints the input line by line to a given file.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: File to write.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``values``: Anything you wish to print to file.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_io_misc/to_file.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_io_misc/to_file.py>`_. 


.. _`module:procgraph_mpl`:


.. rst-class:: procgraph:module

Package ``procgraph_mpl``
============================================================



.. rst-class:: procgraph:desc

Blocks using Matplotlib to display data.

.. _`block:plot`:


.. rst-class:: procgraph:block

Block ``plot``
------------------------------------------------------------------
Plots the inputs using matplotlib. 

This block accepts an arbitrary number of signals.
Each signals is treated independently and plot separately.

Each signal can either be:

1.  A tuple of length 2. It is interpreted as a tuple ``(x,y)``,
    and we plot ``x`` versus ``y`` (see also :ref:`block:make_tuple`).

2.  A list of numbers, or a 1-dimensional numpy array of length N.
    In this case, it is interpreted as the y values,
    and we set  ``x = 1:N``.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width`` (default: 320): Image dimension

- ``height`` (default: 240): Image dimension

- ``xlabel`` (default: None): X label for the plot.

- ``ylabel`` (default: None): Y label for the plot.

- ``legend`` (default: None): List of strings to use as legend handles.

- ``title`` (default: None): If None, use the signal name. Set to ``""`` to disable.

- ``format`` (default: -): Line format ("-",".","x-",etc.)

- ``symmetric`` (default: False): An alternative to y_min, y_max. Makes sure the plot is symmetric for y.

- ``x_min`` (default: None): If set, force the X axis to have this minimum.

- ``x_max`` (default: None): If set, force the X axis to have this maximum.

- ``y_min`` (default: None): If set, force the Y axis to have this minimum.

- ``y_max`` (default: None): If set, force the Y axis to have this maximum.

- ``keep`` (default: False): If True, tries to reuse the figure, without closing. (buggy on some backends)

- ``transparent`` (default: False): If true, outputs a RGBA image instead of RGB.

- ``tight`` (default: False): Uses "tight" option for creating png.

- ``fancy_styles`` (default: []): A list of fancy styles to apply (['notopaxis', 'dickinsonA', 'noxticks', 'noyticks', 'nobottomaxis']).


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Data to plot. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: Resulting image.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_mpl/plot.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_mpl/plot.py>`_. 


.. _`module:procgraph_mplayer`:


.. rst-class:: procgraph:module

Package ``procgraph_mplayer``
============================================================



.. rst-class:: procgraph:desc

Blocks for encoding/decoding video based on MPlayer.

.. _`block:mencoder`:


.. rst-class:: procgraph:block

Block ``mencoder``
------------------------------------------------------------------
Encodes a video stream using ``mencoder``. 

Note that allowed codec and bitrate depend on
your version of mencoder.

MP4 output: currently it works by creating a .AVI with mencoder
and then converting to MP4 using ffmpeg (MP4 support for mencoder
is currently --- Feb'12 --- broken).

RGBA videos: not working fully. For now it outputs .AVI with
mencoder and encoded using png.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: Output file (AVI/MP4 format)

- ``fps`` (default: None): Framerate of resulting movie. If not specified, it will be guessed from data.

- ``fps_safe`` (default: 10): If the frame autodetect gives strange results, we use this safe value instead.

- ``vcodec`` (default: mpeg4): Codec to use.

- ``vbitrate`` (default: 2000000): Bitrate -- default is reasonable.

- ``quiet`` (default: True): If True, suppress mencoder's messages

- ``timestamps`` (default: True): If True, also writes <file>.timestamps that includes a line with the timestamp for each frame

- ``crop`` (default: False): If true, the video will be post-processed and cropped


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``image``: Either a HxWx3 uint8 numpy array representing an RGB image, or a HxW representing grayscale.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_mplayer/mencoder.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_mplayer/mencoder.py>`_. 


.. _`block:mplayer`:


.. rst-class:: procgraph:block

Block ``mplayer``
------------------------------------------------------------------
Decodes a video stream.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: Input video file. This can be in any format that ``mplayer`` understands.

- ``quiet`` (default: True): If true, suppress stderr messages from mplayer.

- ``stats``: If true, writes some statistics about the remaining time.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``video``: RGB stream as numpy array.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_mplayer/mplayer.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_mplayer/mplayer.py>`_. 


.. _`module:procgraph_numpy_ops`:


.. rst-class:: procgraph:module

Package ``procgraph_numpy_ops``
============================================================



.. rst-class:: procgraph:desc

Various operations wrapping numpy functions.

.. _`block:abs`:


.. rst-class:: procgraph:block

Block ``abs``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.absolute`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:arctan`:


.. rst-class:: procgraph:block

Block ``arctan``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.arctan`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:array`:


.. rst-class:: procgraph:block

Block ``array``
------------------------------------------------------------------
Converts the value to a Numpy array.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:astype`:


.. rst-class:: procgraph:block

Block ``astype``
------------------------------------------------------------------
Converts an array using the ``astype`` function.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``dtype``: The new dtype. (string)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: Numpy array (array)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``typed``: The Numpy array with the new type. (array)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:deg2rad`:


.. rst-class:: procgraph:block

Block ``deg2rad``
------------------------------------------------------------------
Converts degrees to radians (wrapper around :np:data:`numpy.radians`.)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:dstack`:


.. rst-class:: procgraph:block

Block ``dstack``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.ma.dstack`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: |towrite|

- ``y``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:fliplr`:


.. rst-class:: procgraph:block

Block ``fliplr``
------------------------------------------------------------------
Flips the array left/right (wrapper for :py:func:`numpy.fliplr`.)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``m``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:flipud`:


.. rst-class:: procgraph:block

Block ``flipud``
------------------------------------------------------------------
Flips the array up/down (wrapper for :py:func:`numpy.flipud`.)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``m``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:gradient1d`:


.. rst-class:: procgraph:block

Block ``gradient1d``
------------------------------------------------------------------
Computes the gradient of a 1D array.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: Numpy array (array(N),N>3)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``typed``: The gradient of the array. (array)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/gradient1d.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/gradient1d.py>`_. 


.. _`block:hstack`:


.. rst-class:: procgraph:block

Block ``hstack``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.ma.hstack`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: |towrite|

- ``y``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:log`:


.. rst-class:: procgraph:block

Block ``log``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.log`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:max`:


.. rst-class:: procgraph:block

Block ``max``
------------------------------------------------------------------
Maximum over **all** elements.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:maximum`:


.. rst-class:: procgraph:block

Block ``maximum``
------------------------------------------------------------------
Limits the numpy array to the given threshold.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``threshold``: |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:mean`:


.. rst-class:: procgraph:block

Block ``mean``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.mean`.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``dtype`` (default: None): |towrite|

- ``axis`` (default: None): |towrite|

- ``out`` (default: None): |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:minimum`:


.. rst-class:: procgraph:block

Block ``minimum``
------------------------------------------------------------------
Limits the numpy array to the given threshold.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``threshold``: |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: Any numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: Array of same shape.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:norm`:


.. rst-class:: procgraph:block

Block ``norm``
------------------------------------------------------------------
Returns the norm of the vector.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``ord`` (default: 2): |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:normalize_Linf`:


.. rst-class:: procgraph:block

Block ``normalize_Linf``
------------------------------------------------------------------
Normalize a vector such that ``|x|_inf = max(abs(x))= 1``.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``normalized``: The same array normalized.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:outer`:


.. rst-class:: procgraph:block

Block ``outer``
------------------------------------------------------------------
Outer product of two vectors. 

This is a wrapper around :py:func:`numpy.multiply.outer`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: First vector.

- ``b``: Second vector.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``outer``: Outer product of the two vectors.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:rad2deg`:


.. rst-class:: procgraph:block

Block ``rad2deg``
------------------------------------------------------------------
Converts radians to degrees (wrapper around :np:data:`numpy.degrees`.)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:real`:


.. rst-class:: procgraph:block

Block ``real``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.real`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``val``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:select`:


.. rst-class:: procgraph:block

Block ``select``
------------------------------------------------------------------
Selects some of the elements of ``x``.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``every``: How many to jump (every=2 takes only the even elements).


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Numpy array that can be flatly addressed.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``decimated``: The decimated output.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:sign`:


.. rst-class:: procgraph:block

Block ``sign``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.sign`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:smooth1d`:


.. rst-class:: procgraph:block

Block ``smooth1d``
------------------------------------------------------------------
Smooth the data using a window with requested size. 

This method is based on the convolution of a scaled window with the signal.
The signal is prepared by introducing reflected copies of the signal
(with the window size) in both ends so that transient parts are minimized
in the begining and end part of the output signal.

``window`` must be one of  'flat', 'hanning', 'hamming', 'bartlett',
'blackman'.
A flat window will produce a moving average smoothing.

example: ::

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

see also:

numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman,
numpy.convolve
scipy.signal.lfilter

TODO: the window parameter could be the window itself if an
      array instead of a string


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``window_len`` (default: 11): the dimension of the smoothing window;  an odd integer

- ``window`` (default: hanning): the type of window from


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: the input signal


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``smoothed``: the smoothed signal


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/smooth1d.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/smooth1d.py>`_. 


.. _`block:square`:


.. rst-class:: procgraph:block

Block ``square``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.square`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:sum`:


.. rst-class:: procgraph:block

Block ``sum``
------------------------------------------------------------------
Sum over **all** elements.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:take`:


.. rst-class:: procgraph:block

Block ``take``
------------------------------------------------------------------
|towrite|


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``indices``: |towrite|

- ``axis`` (default: 0): |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`block:vstack`:


.. rst-class:: procgraph:block

Block ``vstack``
------------------------------------------------------------------
Wrapper around :np:data:`numpy.ma.vstack`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: |towrite|

- ``y``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_numpy_ops/filters.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_numpy_ops/filters.py>`_. 


.. _`module:procgraph_pil`:


.. rst-class:: procgraph:module

Package ``procgraph_pil``
============================================================



.. rst-class:: procgraph:desc

Blocks for image operations based on the PIL library

.. _`block:imread`:


.. rst-class:: procgraph:block

Block ``imread``
------------------------------------------------------------------
Reads an image from a file.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``filename``: Image filename. (string)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``image``: The image as a numpy array. (image)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_pil/imread.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_pil/imread.py>`_. 


.. _`block:imwrite`:


.. rst-class:: procgraph:block

Block ``imwrite``
------------------------------------------------------------------
Writes an image to a file.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_pil/imwrite.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_pil/imwrite.py>`_. 


.. _`block:resize`:


.. rst-class:: procgraph:block

Block ``resize``
------------------------------------------------------------------
Resizes an image. 

You should pass at least one of ``width`` or ``height``.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width`` (default: None): Target image width. (int,>0)

- ``height`` (default: None): Target image height. (int,>0)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: The image to resize. (image)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``image``: The image as a numpy array. (rgb)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_pil/pil_operations.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_pil/pil_operations.py>`_. 


.. _`block:text`:


.. rst-class:: procgraph:block

Block ``text``
------------------------------------------------------------------
This block provides text overlays over an image. 

This block is very powerful, but the configuration is a bit complicated.

You should provide a list of dictionary in the configuration variable
``texts``. Each dictionary in the list describes how and where to write
one piece of text.

An example of valid configuration is the following: ::

    text.texts = [{string: "raw image", position: [10,30], halign: left,
                  color: black, bg: white }]

The meaning of the fields is as follow:

``string``
  Text to display. See the section below about keyword expansion.

``position``
  Array of two integers giving the position of the text in the image

``color``
  Text color. It can be a keyword color or an hexadecimal string
  (``white`` or ``#ffffff``).

``bg``
  background color

``halign``
  Horizontal alignment.
  Choose between ``left`` (default), ``center``, ``right``.

``valign``
  Vertical alignment.
  Choose between ``top`` (default), ``middle``, ``center``.

``size``
  Font size in pixels

``font``
  Font family. Must be a ttf file (``Arial.ttf``)

**Expansion**: Also we expand macros in the text using ``format()``.
The available keywords are:

``frame``
  number of frames since the beginning

``time``
  seconds since the beginning of the log

``timestamp``
  absolute timestamp


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``texts``: Text specification (see block description).


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: Input image.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``rgb``: Output image with overlaid text.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_pil/text.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_pil/text.py>`_. 


.. _`module:procgraph_robotics`:


.. rst-class:: procgraph:module

Package ``procgraph_robotics``
============================================================



.. rst-class:: procgraph:desc

Some functions specific to robotics applications. 


.. rst-class:: procgraph:desc_rest

Requires: http://github.com/AndreaCensi/geometry

.. _`block:laser_display`:


.. rst-class:: procgraph:block

Block ``laser_display``
------------------------------------------------------------------
Produces a plot of a range-finder scan. 

Example of configuration: ::

    display_sick.groups = [{ indices: [0,179], theta: [-1.57,+1.57],
         color: 'r', origin: [0,0,0]}]


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width`` (default: 320): Width of the resulting image.

- ``height`` (default: 320): Height of the resulting image.

- ``max_readings`` (default: 30): Readings are clipped at this threshold (m).

- ``groups``: How to group and draw the readings. (see example)

- ``title`` (default: None): By default it displays the signal name. Set the empty string to disable.

- ``transparent`` (default: False): Gives transparent RGBA rather than RGB.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``readings``: The laser readings (array of floats).


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``image``: The laser visualization (rgba).


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_robotics/laser_display.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_robotics/laser_display.py>`_. 


.. _`block:laser_dot_display`:


.. rst-class:: procgraph:block

Block ``laser_dot_display``
------------------------------------------------------------------
Produces a plot of a range-finder scan variation (derivative). 

It is a variation of :ref:`block:laser_display`; look there for
the documentation.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``width`` (default: 320): Width of the resulting image.

- ``height`` (default: 320): Height of the resulting image.

- ``groups``: How to group and draw the readings.  (see :ref:`block:laser_display`)

- ``title`` (default: None): By default it displays the signal name. Set the empty string to disable.

- ``transparent`` (default: False): Gives transparent RGBA rather than RGB.

- ``R0`` (default: 1): Radius of the readings circle.

- ``amp`` (default: 0.5): Amplitude of the readings crown.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``readings_dot``: Array of float representing array readings.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``image``: A fancy visualization of the laser derivative


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_robotics/laser_dot_display.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_robotics/laser_dot_display.py>`_. 


.. _`block:organic_scale`:


.. rst-class:: procgraph:block

Block ``organic_scale``
------------------------------------------------------------------
A (almost failed!) attempt to scale a signal into [-1,1] according to the history. 

This one is a mess.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``skim`` (default: 5): |towrite|

- ``skim_hist`` (default: 5): |towrite|

- ``hist`` (default: 100): How many steps of history to use.

- ``tau`` (default: 0.1): |towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value_scaled``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_robotics/organic_scale.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_robotics/organic_scale.py>`_. 


.. _`block:pose2commands`:


.. rst-class:: procgraph:block

Block ``pose2commands``
------------------------------------------------------------------
Computes the velocity commands from the odometry data.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``pose``: Odometry as an array ``[x,y,theta]``.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``commands``: Estimated commands as an array ``[vx,vy,omega]``.

- ``vx``: Linear velocity, forward (m/s)

- ``vy``: Linear velocity, side (m/s)

- ``omega``: Angular velocity (rad/s)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_robotics/pose2velocity.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_robotics/pose2velocity.py>`_. 


.. _`block:pose2vel_`:


.. rst-class:: procgraph:block

Block ``pose2vel_``
------------------------------------------------------------------
Block used by :ref:`block:pose2commands`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``q12``: Last two poses.

- ``t12``: Last two timestamps.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``commands``: Estimated commands ``[vx,vy,omega]``.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_robotics/pose2velocity.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_robotics/pose2velocity.py>`_. 


.. _`block:skim`:


.. rst-class:: procgraph:block

Block ``skim``
------------------------------------------------------------------
Cuts off the top and bottom percentile of the array.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``percent`` (default: 5): How much to cut off (decimal). (float,>=0,<90)


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``a``: Any numpy array. (array[x])


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: Skimmed version of ``a``. (array[x])


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_robotics/misc.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_robotics/misc.py>`_. 


.. _`module:procgraph_ros`:


.. rst-class:: procgraph:module

Package ``procgraph_ros``
============================================================



.. rst-class:: procgraph:desc

This is a set of blocks to read and write logs in ROS_ Bag format. 


.. rst-class:: procgraph:desc_rest

You need the `rospy` package to be installed.

.. _pytables: http://pytables.org

.. _ROS: http://www.ros.org

.. _`block:bagread`:


.. rst-class:: procgraph:block

Block ``bagread``
------------------------------------------------------------------
This block reads a bag file (ROS logging format).


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: Bag file to read

- ``topics`` (default: None): Which signals to output (and in what order). Should be a comma-separated list. If you do not specify it (or if empty) it will be all signals.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The signals read from the log. (signals are defined at runtime)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_ros/bagread.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_ros/bagread.py>`_. 


.. _`block:bagread_test`:


.. rst-class:: procgraph:block

Block ``bagread_test``
------------------------------------------------------------------
Test of the bagread block.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: .bag file to read

- ``topics``: topics to read


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_ros/models/bagread_test.pg <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_ros/models/bagread_test.pg>`_. 


.. _`block:bagwrite`:


.. rst-class:: procgraph:block

Block ``bagwrite``
------------------------------------------------------------------
This block writes the incoming signals to a ROS bag file. 

By default, the signals are organized as follows: ::

     /            (root)
     /procgraph             (group with name procgraph)
     /procgraph/signal1     (table)
     /procgraph/signal2     (table)
     ...


Note that the input should be ROS messages; no conversion is done.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``file``: Bag file to write


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to be written (variable number: n >= 1)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_ros/bagwrite.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_ros/bagwrite.py>`_. 


.. _`block:ros2python`:


.. rst-class:: procgraph:block

Block ``ros2python``
------------------------------------------------------------------
Converts a ROS message to a Python object.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``msg``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_ros/conversions.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_ros/conversions.py>`_. 


.. _`block:ros_scan2python`:


.. rst-class:: procgraph:block

Block ``ros_scan2python``
------------------------------------------------------------------
|towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``scan``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_ros/conversions.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_ros/conversions.py>`_. 


.. _`module:procgraph_signals`:


.. rst-class:: procgraph:module

Package ``procgraph_signals``
============================================================



.. rst-class:: procgraph:desc

Blocks performing operations with a dynamic nature. 


.. rst-class:: procgraph:desc_rest

This library contains blocks that perform operations with time.

.. _`block:any`:


.. rst-class:: procgraph:block

Block ``any``
------------------------------------------------------------------
Joins the stream of multiple signals onto one output signal.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to be put on the same stream. (variable number: n >= 1)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``stream``: Unified stream.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/any.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/any.py>`_. 


.. _`block:async`:


.. rst-class:: procgraph:block

Block ``async``
------------------------------------------------------------------
|towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to (a)synchronize. The first is the master. (variable number: n >= 2)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Synchronized signals. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/async.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/async.py>`_. 


.. _`block:derivative`:


.. rst-class:: procgraph:block

Block ``derivative``
------------------------------------------------------------------
Computes the derivative of a quantity with 3 taps  (``x[t+1] - x[t-1]``). See also :ref:`block:derivative2`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: quantity to derive


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x_dot``: approximate derivative


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/derivative.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/derivative.py>`_. 


.. _`block:derivative2`:


.. rst-class:: procgraph:block

Block ``derivative2``
------------------------------------------------------------------
Computes the derivative of a quantity with 2 taps (``x[t+1] - x[t]``). See also :ref:`block:derivative`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: quantity to derive


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x_dot``: approximate derivative


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/derivative2.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/derivative2.py>`_. 


.. _`block:extract`:


.. rst-class:: procgraph:block

Block ``extract``
------------------------------------------------------------------
This block extracts some of the components of a vector. 

Example: Extracts the first and third component of x. ::

    x -> |extract index=[0,2]| -> x_part


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``index``: Index (or indices) to extract.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``vector``: Any numpy array


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``part``: The part extracted


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/extract.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/extract.py>`_. 


.. _`block:forward_difference`:


.. rst-class:: procgraph:block

Block ``forward_difference``
------------------------------------------------------------------
Computes ``x[t+1] - x[t-1]`` normalized with timestamp. 

You want to attach this to :ref:`block:last_n_samples`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x123``: An array with the last 3 values of x.

- ``t123``: An array with the last 3 values of the timestamp.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x_dot``: Derivative of x


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/derivative.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/derivative.py>`_. 


.. _`block:fps_data_limit`:


.. rst-class:: procgraph:block

Block ``fps_data_limit``
------------------------------------------------------------------
This block limits the output update to a certain framerate.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``fps``: Maximum framerate.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to decimate. (variable number: n >= 1)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Decimated signals. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/fps_data_limit.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/fps_data_limit.py>`_. 


.. _`block:fps_limit`:


.. rst-class:: procgraph:block

Block ``fps_limit``
------------------------------------------------------------------
This block limits the output update to a certain *realtime* framerate. 

Note that this uses realtime wall clock time -- not the data time!
This is mean for real-time applications, such as visualization.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``fps``: Realtime fps limit.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Arbitrary signals. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Arbitrary signals with limited framerate. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/fps_limit.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/fps_limit.py>`_. 


.. _`block:fps_print`:


.. rst-class:: procgraph:block

Block ``fps_print``
------------------------------------------------------------------
Prints the fps count for the input signals.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Any signal. (variable number: n >= 1)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/fps_print.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/fps_print.py>`_. 


.. _`block:history`:


.. rst-class:: procgraph:block

Block ``history``
------------------------------------------------------------------
This block collects the history of a quantity, and outputs two signals ``x`` and ``t``. See also :ref:`block:historyt` and :ref:`block:last_n_samples`.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``interval`` (default: 10): Length of the interval to record.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``values``: Any signal.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Sequence of values.

- ``t``: Sequence of timestamps.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/history.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/history.py>`_. 


.. _`block:historyt`:


.. rst-class:: procgraph:block

Block ``historyt``
------------------------------------------------------------------
This block collects the signals samples of a signals, and outputs *one* signal containing a tuple  ``(t,x)``. See also :ref:`block:last_n_samples` and :ref:`block:history`. 

If ``natural`` is true, it uses the time from the beginning of the log.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``interval`` (default: 10): Length of interval (seconds).

- ``natural`` (default: True): If true, set 0 to be timestamp of the log beginning. This allows to have prettier graphs


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any signal.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``history``: Tuple ``(t,x)`` containing two arrays.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/historyt.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/historyt.py>`_. 


.. _`block:join`:


.. rst-class:: procgraph:block

Block ``join``
------------------------------------------------------------------
This block joins multiple signals into one.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to be joined together. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``joined``: Joined signals.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/join.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/join.py>`_. 


.. _`block:last_n_samples`:


.. rst-class:: procgraph:block

Block ``last_n_samples``
------------------------------------------------------------------
This block collects the last N samples of a signals, and outputs two signals ``x`` and ``t``. See also :ref:`block:historyt` and :ref:`block:history`.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``n``: Number of samples to retain.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any data


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Sequence of values.

- ``t``: Sequence of timestamps.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/last_n_samples.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/last_n_samples.py>`_. 


.. _`block:low_pass`:


.. rst-class:: procgraph:block

Block ``low_pass``
------------------------------------------------------------------
Implements simple low-pass filtering. 

Formula used: ::

    y[k] = alpha * u[k] + (1-alpha) * y[k-1]


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``alpha``: Innovation rate


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``value``: Any numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``lowpass``: The lowpass version.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/low_pass.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/low_pass.py>`_. 


.. _`block:make_tuple`:


.. rst-class:: procgraph:block

Block ``make_tuple``
------------------------------------------------------------------
Creates a tuple out of the input signals values. 

Often used for plotting two signals as (x,y); see :ref:`block:plot`.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to unite in a tuple. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``tuple``: Tuple containing signals.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/make_tuple.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/make_tuple.py>`_. 


.. _`block:sieve`:


.. rst-class:: procgraph:block

Block ``sieve``
------------------------------------------------------------------
This block decimates the data in time by transmitting only one in ``n`` updates.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``n``: Decimation level; ``n = 3`` means transmit one in three.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``data``: Arbitrary input signals.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``decimated``: Decimated signals.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/sieve.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/sieve.py>`_. 


.. _`block:slice`:


.. rst-class:: procgraph:block

Block ``slice``
------------------------------------------------------------------
Slices a signal by extracting from index ``start`` to index ``end`` (INCLUSIVE).


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``start``: Slice start.

- ``end``: Slice end (inclusive).


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``signal``: Any 1d numpy array


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``sliced``: The sliced signal.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/extract.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/extract.py>`_. 


.. _`block:sync`:


.. rst-class:: procgraph:block

Block ``sync``
------------------------------------------------------------------
This block synchronizes a set of streams to the first stream (the master). 

The first signal is called the "master" signal.
The other (N-1) are slaves.

We guarantee that:

- if the slaves are faster than the master,
  then we output exactly the same.

Example diagrams: ::

    Master  *  *  *   *   *
    Slave   ++++++++++++++++

    Master  *  *  *   *   *
    output? v  v  x   v
    Slave   +    +      +
    output? v    v      v


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Signals to synchronize. The first is the master. (variable number: n >= 2)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Synchronized signals. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/sync.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/sync.py>`_. 


.. _`block:two_step_difference`:


.. rst-class:: procgraph:block

Block ``two_step_difference``
------------------------------------------------------------------
Computes ``x[t+1] - x[t]`` normalized with timestamp.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x12``: An array with the last 2 values of x.

- ``t12``: An array with the last 2 values of the timestamp.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x_dot``: Derivative of x


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/derivative2.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/derivative2.py>`_. 


.. _`block:wait`:


.. rst-class:: procgraph:block

Block ``wait``
------------------------------------------------------------------
This block waits a given number of updates before transmitting the output signal.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``n``: Number of updates to wait at the beginning.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Arbitrary signals. (variable number)


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Copy of the signals, minus the first *n* updates. (variable number)


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_signals/wait.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_signals/wait.py>`_. 


.. _`module:procgraph_statistics`:


.. rst-class:: procgraph:module

Package ``procgraph_statistics``
============================================================



.. rst-class:: procgraph:desc

Blocks for common statistical operations.

.. _`block:cov2corr`:


.. rst-class:: procgraph:block

Block ``cov2corr``
------------------------------------------------------------------
Compute the correlation matrix from the covariance matrix. If zero_diagonal = True, the diagonal is set to 0 instead of 1.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``zero_diagonal`` (default: True): Whether to set the (noninformative) diagonal to zero.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``covariance``: A 2D numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``correlation``: The exctracted correlation.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/cov2corr.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/cov2corr.py>`_. 


.. _`block:covariance`:


.. rst-class:: procgraph:block

Block ``covariance``
------------------------------------------------------------------
Computes the covariance matrix of the input.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``wait`` (default: 10): Number of sample to have reliable expectation.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Unidimensional numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``cov_x``: Square matrix representing sample covariance.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/covariance.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/covariance.py>`_. 


.. _`block:expectation`:


.. rst-class:: procgraph:block

Block ``expectation``
------------------------------------------------------------------
Computes the sample expectation of a signal.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``Ex``: Expectation of input.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/expectation.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/expectation.py>`_. 


.. _`block:maximum_over_time`:


.. rst-class:: procgraph:block

Block ``maximum_over_time``
------------------------------------------------------------------
Computes the minimum of a signal over time.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``max_x``: Maximum of input over time.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/minimum.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/minimum.py>`_. 


.. _`block:minimum_over_time`:


.. rst-class:: procgraph:block

Block ``minimum_over_time``
------------------------------------------------------------------
Computes the minimum of a signal over time.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``min_x``: Minimum of input.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/minimum.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/minimum.py>`_. 


.. _`block:normalize`:


.. rst-class:: procgraph:block

Block ``normalize``
------------------------------------------------------------------
Removes the mean from a signal.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``wait`` (default: 10): Number of sample to have reliable expectation.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Unidimensional numpy array.


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x_n``: Signal without the mean.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/covariance.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/covariance.py>`_. 


.. _`block:soft_variance`:


.. rst-class:: procgraph:block

Block ``soft_variance``
------------------------------------------------------------------
Computes the element-wise "soft" variance (exp. of error abs. value)


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``wait`` (default: 100): Number of samples to wait before declaring the value valid.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any numpy array


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``var_x``: Soft variance of ``x``.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/variance.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/variance.py>`_. 


.. _`block:variance`:


.. rst-class:: procgraph:block

Block ``variance``
------------------------------------------------------------------
Computes the element-wise variance.


.. rst-class:: procgraph:config

Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``wait`` (default: 100): Number of samples to wait before declaring the value valid.


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``x``: Any numpy array


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``var_x``: Variance of ``x``.


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_statistics/variance.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_statistics/variance.py>`_. 


.. _`module:procgraph_yaml`:


.. rst-class:: procgraph:module

Package ``procgraph_yaml``
============================================================



.. rst-class:: procgraph:desc

YAML conversions.

.. _`block:yaml2object`:


.. rst-class:: procgraph:block

Block ``yaml2object``
------------------------------------------------------------------
|towrite|


.. rst-class:: procgraph:input

Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``s``: |towrite|


.. rst-class:: procgraph:output

Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``0``: |towrite|


.. rst-class:: procgraph:source

Implemented in `/src/procgraph_yaml/yaml2object.py <https://github.com/AndreaCensi/procgraph/blob/master//src/procgraph_yaml/yaml2object.py>`_. 


