===============================
fitsiochunked
===============================

.. image:: https://img.shields.io/travis/mindriot101/fitsiochunked.svg
        :target: https://travis-ci.org/mindriot101/fitsiochunked

Package to *sequentially* efficiently read large fits arrays in object by object

* Free software: MIT license

Features
--------

* *Sequentially* read in large fits files, within a given fixed memory limit

Quick usage
-----------

The following example shows an example of reading in a large fits
hdu within a memory limit of 2048MB, assuming light curves are
stored in rows:

.. code:: python

  import numpy as np
  import fitsio
  import fitsiochunked as fc

  with fitsio.FITS(filename) as infile:
      hdu = infile['flux']
      napertures = hdu.get_info()['ndim'][0]
      mean_flux = np.zeros(napertures)

      for chunk in fc.chunks(hdu, memory_limit_mb=2048):

          # `chunk` is a namedtuple with `.data` and `.slice` properties
          chunk_data = chunk.data
          print('Data shape:', chunk_data.shape)
          print('Data dtype:', chunk_data.dtype)


          chunk_slice = chunk.slice
          print('Chunk starting from aperture:', chunk_slice.start)
          print('Chunk up to:', chunk_slice.stop)

          chunk_mean = np.average(chunk_data, axis=1)
          mean_flux[chunk_slice] = chunk_mean

The library copes with an aribtrary number of hdus:

.. code:: python

  import numpy as np
  import fitsio
  import fitsiochunked as fc

  with fitsio.FITS(filename) as infile:
      hjd_hdu = infile['hjd']
      flux_hdu = infile['flux']
      fluxerr_hdu = infile['fluxerr']

      napertures = flux_hdu.get_info()['ndim'][0]
      mean_flux = np.zeros(napertures)

      for chunks in fc.chunks(hjd_hdu, flux_hdu, fluxerr_hdu, memory_limit_mb=2048):
          # chunks is a tuple of chunks
          hjd_chunk, flux_chunk, fluxerr_chunk = chunks

          # `chunk` is a namedtuple with `.data` and `.slice` properties
          flux_chunk_data = flux_chunk.data
          print('Data shape:', flux_chunk_data.shape)
          print('Data dtype:', flux_chunk_data.dtype)

          # and so on

Note: if multiple hdus are supplied, then the ``memory_limit_mb`` and
``chunksize`` arguments to ``chunks`` apply to **each** HDU i.e. three HDUs and
a memory limit of 2048MB will lead to 3x2048 = 6144MB of memory used.

Installation
------------

Install with ``pip``:

.. code:: bash

    pip install fitsiochunked
    # or get the latest development version from github
    pip install git+https://github.com/mindriot101/fitsiochunked

or download and run the setup file:

.. code:: bash

    git clone https://github.com/mindriot101/fitsiochunked
    cd fitsiochunked
    python setup.py install

Details
-------

The high level interface is the ``chunks`` function, which builds a
``ChunkedAdapter`` object wrapping a ``fitsio.ImageHDU`` object.

The ``ChunkedAdapter`` wraps a ``fitsio`` HDU object. When constructed,
it becomes a callable which yields the image data in that hdu in chunks.

The chunksize can be set either with with the parameter
``chunksize`` which simply yields ``chunksize`` rows each time,
or with ``memory_limit_mb`` which *tries* (no promises!) to
automatically calculate the number of lightcurves that will fit into
``memory_limit_mb`` megabytes of memory.


