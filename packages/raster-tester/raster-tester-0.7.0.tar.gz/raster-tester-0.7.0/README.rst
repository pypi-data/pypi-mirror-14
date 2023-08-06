raster-tester
=============

|PyPI| |Circle CI| |codecov.io|

::

     _______________        _______________
    |_|_|_|_|_|_|_|_|      |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| HIRU |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| DIFF |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| FROM |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| ===> |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_|      |_|_|_|_|_|_|_|_|

::

    raster-tester [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      compare
      crossesdateline
      isaligned
      isempty
      istiled

``compare``
-----------

::

    Usage: raster-tester compare [OPTIONS] INPUT_1 INPUT_2

    Options:
      -p, --pixel-threshold INTEGER  Threshold for pixel diffs [default=0]
      -d, --downsample INTEGER       Downsample via decimated read for faster
                                     comparison, and to handle variation in
                                     compression artifacts [default=1]
      -u, --upsample INTEGER         Upsample to handle variation in compression
                                     artifacts [default=1]
      --compare-masked               Only compare masks + unmasked areas of RGBA
                                     rasters
      --no-error                     Compare in non stderr mode: echos "(ok|not
                                     ok) - <input_1> is (within|not within)
                                     <pixel-threshold> pixels of <input 2>"
      --debug                        Print ascii preview of errors
      --flex-mode                    Allow comparison of masked RGB + RGBA
      --help                         Show this message and exit.

``crossesdateline``
-------------------

::

    Usage: raster-tester crossesdateline [OPTIONS] INPUT

    Options:
      --help  Show this message and exit.

``isaligned``
-------------

::

    Usage: raster-tester isaligned [OPTIONS] SOURCES...

    Options:
      --help  Show this message and exit.

``isempty``
-----------

::

    Usage: raster-tester isempty [OPTIONS] INPUT_1

    Options:
      -b, --bidx INTEGER            Check one band
      --randomize                   Iterate through windows in a psuedorandom fashion
      --help                        Show this message and exit.

``istiled``
-----------

::

    Usage: raster-tester istiled [OPTIONS] SOURCES...

    Options:
      --blocksize / --no-blocksize  assert that sources are internally tiled
      --help                        Show this message and exit.

.. |PyPI| image:: https://img.shields.io/pypi/v/raster-tester.svg
   :target: 
.. |Circle CI| image:: https://circleci.com/gh/mapbox/raster-tester.svg?style=shield&circle-token=b160fc4bebd1e032df32fe8c4aff4bbea685701d
   :target: https://circleci.com/gh/mapbox/raster-tester
.. |codecov.io| image:: https://codecov.io/github/mapbox/raster-tester/coverage.svg?branch=master&token=Gz7rJmDH5d
   :target: https://codecov.io/github/mapbox/raster-tester?branch=master
