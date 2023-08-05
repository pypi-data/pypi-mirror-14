#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fitsiochunked
----------------------------------

Tests for `fitsiochunked` module.
"""

import pytest
import fitsio
import numpy as np
from .context import fitsiochunked

@pytest.fixture(scope='session')
def filename():
    return 'test.fits'

@pytest.fixture(scope='session')
def data():
    return np.random.randint(0, 10, size=(100, 50))


@pytest.fixture
def hduname():
    return 'flux'


@pytest.yield_fixture
def hdulist(filename, tmpdir, data, hduname):
    fname = str(tmpdir.join(filename))
    with fitsio.FITS(fname, 'rw', clobber=True) as outfile:
        outfile.write(data, extname=hduname)
        yield outfile

@pytest.fixture
def chunker(hdulist, hduname):
    hdu = hdulist[hduname]
    return fitsiochunked.ChunkedAdapter(hdu)


def test_number_of_rows(chunker, data):
    assert chunker.nrows == data.shape[0]


def test_number_of_images(chunker, data):
    assert chunker.num_images == data.shape[1]


def test_data_type(chunker):
    assert chunker.data_type == 32


def test_chunk_value_object(chunker):
    next_chunk = next(chunker(chunksize=10))
    assert hasattr(next_chunk, 'data') and hasattr(next_chunk, 'slice')


def test_chunk_size(chunker):
    next_chunk = next(chunker(chunksize=10))
    assert next_chunk.data.shape[0] == 10


@pytest.mark.parametrize('chunksize,nchunks', [
    (50, 2),
    (100, 1),
    (10, 10),
    (1, 100),
    (99, 2),
])
def test_number_of_chunks(chunker, chunksize, nchunks):
    chunks = list(chunker(chunksize=chunksize))
    assert len(chunks) == nchunks


@pytest.mark.parametrize('chunksize', [
    50, 100, 10, 1, 99
])
def test_chunk_contents(chunker, data, chunksize):
    chunks = list(chunker(chunksize=chunksize))
    for i in range(len(chunks)):
        assert (chunks[i].data == data[i * chunksize: (i + 1) * chunksize]).all()


def test_uneven_chunks(chunker):
    chunksize=99
    chunks = list(chunker(chunksize=chunksize))
    assert chunks[0].data.shape[0] == 99
    assert chunks[1].data.shape[0] == 1


@pytest.mark.parametrize('dtype_size, expected', [
    (32, 4),
    (-32, 4),
    (-64, 8),
])
def test_get_image_data_type_size(chunker, dtype_size, expected):
    assert chunker._byte_size(dtype_size) == expected


def test_get_lc_size(chunker, data):
    assert chunker.lc_bytes == data.shape[1] * 4


def test_error_with_no_chunksize_or_memory_limit(chunker):
    with pytest.raises(ValueError) as err:
        _ = list(chunker())
    assert 'supply either chunksize or memory_limit' in str(err)

def test_no_error_with_either_argument(chunker):
    assert list(chunker(memory_limit_mb=1024))
    assert list(chunker(chunksize=10))

@pytest.mark.parametrize('memory_limit_mb, expected', [
    (2, 524288),
    (100, 26214400),
])
def test_memory_limit(chunker, memory_limit_mb, expected):
    assert chunker._max_num_lightcurves(memory_limit_mb) == expected


def test_memory_to_lightcurves(chunker, data):
    memory = 2048
    expected = int((memory * 1024 * 1024 / 4) / data.shape[1])
    assert chunker._memory_to_lightcurves(memory) == expected


def test_chunker_returns_indexes(chunker):
    chunk_size = 50
    chunk = next(chunker(chunksize=chunk_size))
    assert chunk.slice == slice(0, chunk_size, None)


def test_convenience_function(hdulist, data):
    hdu = hdulist[0]
    chunk = next(fitsiochunked.chunks(hdu, chunksize=10))
    assert chunk.data.shape == (10, data.shape[1])


def test_multiple_hdus(tmpdir, filename):
    shape = (100, 10)
    hjd_data = np.random.randint(50, 100, size=shape)
    flux_data = np.random.randint(50, 100, size=shape)
    fluxerr_data = np.random.randint(50, 100, size=shape)

    fname = str(tmpdir.join(filename))
    with fitsio.FITS(fname, 'rw', clobber=True) as outfile:
        outfile.write(hjd_data, extname='hjd')
        outfile.write(flux_data, extname='flux')
        outfile.write(fluxerr_data, extname='fluxerr')

    with fitsio.FITS(fname) as infile:
        hjd = infile['hjd']
        flux = infile['flux']
        fluxerr = infile['fluxerr']

        counter = 0
        for chunk in fitsiochunked.chunks(hjd, flux, fluxerr, chunksize=10):
            hjd, flux, fluxerr = chunk
            assert hjd.data.shape == flux.data.shape == fluxerr.data.shape == (10, shape[1])
            assert (hjd.data == hjd_data[hjd.slice]).all()
            assert (flux.data == flux_data[flux.slice]).all()
            assert (fluxerr.data == fluxerr_data[fluxerr.slice]).all()

            counter += 1

    assert counter == 10

'''
Expected API

with fitsio.FITS(filename) as infile:
    hdu = infile['flux']
    for chunk in fitsiochunked.chunks(hdu, chunksize=10):
        # do something with chunk

    # or the low level api
    chunker = fitsiochunked.ChunkedAdapter(hdu)
    for chunk in chunker(chunksize=10): # or chunker(memory_limit=2048)
        # do something with chunk

# Multiple HDUs simultaneously

with fitsio.FITS(filename) as infile:
    hjd = infile['hjd']
    flux = infile['flux']
    fluxerr = infile['fluxerr']

    for every in fitsiochunked.chunks(hjd, flux, fluxerr, chunksize=10):
        # every.hjd.data, every.flux.data, every.fluxerr.data
'''
