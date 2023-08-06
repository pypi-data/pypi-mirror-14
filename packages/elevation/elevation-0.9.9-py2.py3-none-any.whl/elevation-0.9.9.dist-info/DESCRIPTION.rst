Global geographic elevation data made easy.
Elevation provides easy download, cache and access of the global datasets
`SRTM 30m Global 1 arc second V003 <https://lpdaac.usgs.gov/dataset_discovery/measures/measures_products_table/SRTMGL1_v003>`_
elaborated by NASA and NGA
and
`SRTM 90m Digital Elevation Database v4.1 <http://www.cgiar-csi.org/data/srtm-90m-digital-elevation-database-v4-1>`_
elaborated by CGIAR-CSI.

Note that any download policies of the respective providers apply.


Installation
------------

Install the `latest version of Elevation <https://pypi.python.org/pypi/elevation>`_
from the Python Package Index::

    $ pip install elevation

The following dependencies need to be installed and working:

- `GNU make <https://www.gnu.org/software/make/>`_
- `curl <https://curl.haxx.se/>`_
- unzip
- `GDAL command line tools <http://www.gdal.org/>`_

The following command runs some basic checks and reports common issues::

    $ eio selfcheck
    Your system is ready.

GNU make, curl and unzip come pre-installed with most operating systems.
The best way to install GDAL command line tools varies across operating systems
and distributions, please refer to the
`GDAL install documentation <https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries>`_.


Command line usage
------------------

Identify the geographic bounds of the area of interest and fetch the DEM with the ``eio`` command.
For example to clip the SRTM1 30m DEM of Rome, around 41.9N 12.5W, to the ``Rome-DEM.tif`` file::

    $ eio clip -o Rome-DEM.tif --bounds 12.35 41.8 12.65 42

The ``--bounds`` option accepts latitude and longitude coordinates
(more precisely in geodetic coordinates in the WGS84 refernce system EPSG:4326 for those who care)
given as ``left bottom right top`` similarly to the ``rio`` command form ``rasterio``.

The first time an area is accessed Elevation downloads the data tiles from the USGS or CGIAR-CSI servers and
caches them in GeoTiff compressed formats,
subsequent accesses to the same and nearby areas are much faster.

It is possible to pre-populate the cache for an area, for example to seed the SRTM3 90m DEM of
a wider area around Rome execute::

    $ eio --product SRTM3 seed --bounds 10.5 40 14.5 44

The ``seed`` sub-command doesn't allow automatic download of a large amount of DEM tiles,
please refer to the upstream providers' websites to learn the preferred procedures for bulk download.

To clean up stale temporary files and to try fixing the cache in the event of a server error use::

    $ eio --product SRTM3 clean

The ``eio`` command as the following sub-commands and options::

    $ eio --help
    Usage: eio [OPTIONS] COMMAND [ARGS]...

    Options:
      --product [SRTM1|SRTM3]  DEM product choice (default: 'SRTM1').
      --cache_dir DIRECTORY    Root of the DEM cache folder (default: [...]).
      --make_flags TEXT        Options to be passed to make (default: '-k').
      --help                   Show this message and exit.

    Commands:
      clean      Clean up the cache from temporary files.
      clip       Clip the DEM to given bounds.
      distclean  Clean up the cache from temporary files.
      info
      seed       Seed the DEM to given bounds.
      selfcheck  Audits your installation for common issues.

The ``seed`` sub-command::

    $ eio seed --help
    Usage: eio seed [OPTIONS]

    Options:
      --bounds FLOAT...  Output bounds: left bottom right top.
      --help             Show this message and exit.

The ``clip`` sub-command::

    $ eio clip --help
    Usage: eio clip [OPTIONS]

    Options:
      -o, --output PATH  Path to output file. Existing files will be overwritten.
      --bounds FLOAT...  Output bounds: left bottom right top.
      --help             Show this message and exit.


Python API
----------

Every command has a corresponding API function in the ``elevation`` module::

    import elevation

    # clip the SRTM1 30m DEM of Rome and save it to Rome-DEM.tif
    elevation.clip(bounds=(12.35, 41.8, 12.65, 42), output='Rome-DEM.tif')

    # seed the SRTM3 90m DEM of a wider area around Rome
    elevation.seed(product='SRTM3', bounds=(10.5, 40, 14.5, 44))


Project resources
-----------------

============= =========================================================
Documentation http://elevation.bopen.eu
Support       https://stackoverflow.com/search?q=python+elevation
Development   https://github.com/bopen/elevation
Download      https://pypi.python.org/pypi/elevation
Code quality  .. image:: https://api.travis-ci.org/bopen/elevation.svg?branch=master
                :target: https://travis-ci.org/bopen/elevation/branches
                :alt: Build Status on Travis CI
              .. image:: https://coveralls.io/repos/bopen/elevation/badge.svg?branch=master&service=github
                :target: https://coveralls.io/github/bopen/elevation
                :alt: Coverage Status on Coveralls
============= =========================================================


Contributing
------------

Contributions are very welcome. Please see the `CONTRIBUTING`_ document for
the best way to help.
If you encounter any problems, please file an issue along with a detailed description.

.. _`CONTRIBUTING`: https://github.com/bopen/elevation/blob/master/CONTRIBUTING.rst

Authors:

- B-Open Solutions srl - `@bopen <https://github.com/bopen>`_ - http://bopen.eu
- Alessandro Amici - `@alexamici <https://github.com/alexamici>`_


License
-------

Elevation is free and open source software
distributed under the terms of the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.


