# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy.tests.helper import pytest
from astropy.io import fits
from astropy.wcs import WCS
from astropy.units import Quantity
from ...utils.testing import requires_dependency, requires_data
from ...datasets import FermiGalacticCenter
from ...data import DataStore
from ...utils.energy import EnergyBounds
from ...cube import SkyCube
from ...image import (
    binary_disk,
    binary_ring,
    separation,
    make_header,
    contains,
    solid_angle,
    images_to_cube,
    cube_to_image,
    block_reduce_hdu,
    wcs_histogram2d,
    lon_lat_rectangle_mask,
    SkyMap,
)


def test_binary_disk():
    actual = binary_disk(1)
    desired = np.array([[False, True, False],
                        [True, True, True],
                        [False, True, False]])
    assert_equal(actual, desired)


def test_binary_ring():
    actual = binary_ring(1, 2)
    desired = np.array([[False, False, True, False, False],
                        [False, True, True, True, False],
                        [True, True, False, True, True],
                        [False, True, True, True, False],
                        [False, False, True, False, False]])
    assert_equal(actual, desired)


class TestImageCoordinates(object):
    def setup_class(self):
        self.image = SkyMap.empty(nxpix=3, nypix=2, binsz=10, proj='CAR').to_image_hdu()
        self.image.data = np.arange(3 * 2).reshape(self.image.data.shape)

    def test_separation(self):
        actual = separation(self.image, (1, 0))
        actual = separation(self.image, (0, 90))
        # TODO: assert

    @pytest.mark.xfail
    def test_contains(self):
        # world coordinates
        assert contains(self.image, 0, 0) == True
        assert contains(self.image, 14.9, -9.9) == True
        assert contains(self.image, 20, 0) == False
        assert contains(self.image, 0, -15) == False

        # pixel coordinates
        assert contains(self.image, 0.6, 0.6, world=False) == True
        assert contains(self.image, 3.4, 2.4, world=False) == True
        assert contains(self.image, 0.4, 0, world=False) == False
        assert contains(self.image, 0, 2.6, world=False) == False

        # one-dimensional arrays
        x, y = np.arange(4), np.arange(4)
        inside = contains(self.image, x, y, world=False)
        assert_equal(inside, np.array([False, True, True, False]))

        # two-dimensional arrays
        x = y = np.zeros((3, 2))
        inside = contains(self.image, x, y)
        assert_equal(inside, np.ones((3, 2), dtype=bool))

    # TODO: this works on my machine, but fails for unknown reasons
    # with an IndexError with the `numpy` used here:
    # https://travis-ci.org/gammapy/gammapy/jobs/26836201#L1123
    @pytest.mark.xfail
    def test_image_area(self):
        actual = solid_angle(self.image)
        expected = 99.61946869
        assert_allclose(actual, expected)


@pytest.mark.xfail
def test_process_image_pixels():
    """Check the example how to implement convolution given in the docstring"""
    from astropy.convolution import convolve as astropy_convolve

    def convolve(image, kernel):
        """Convolve image with kernel"""
        from ..utils import process_image_pixels
        images = dict(image=np.asanyarray(image))
        kernel = np.asanyarray(kernel)
        out = dict(image=np.empty_like(image))

        def convolve_function(images, kernel):
            value = np.sum(images['image'] * kernel)
            return dict(image=value)

        process_image_pixels(images, kernel, out, convolve_function)
        return out['image']

    random_state = np.testing.RandomState(seed=0)

    image = random_state.uniform(size=(7, 10))
    kernel = random_state.uniform(size=(3, 5))
    actual = convolve(image, kernel)
    desired = astropy_convolve(image, kernel, boundary='fill')
    assert_allclose(actual, desired)


@requires_dependency('skimage')
class TestBlockReduceHDU():
    def setup_class(self):
        # Arbitrarily choose CAR projection as independent from tests
        projection = 'CAR'
        # Create test image
        self.image = SkyMap.empty(nxpix=12, nypix=8, proj=projection).to_image_hdu()
        self.image.data = np.ones(self.image.data.shape)
        # Create test cube
        self.indices = np.arange(4)
        self.cube_images = []
        for _ in self.indices:
            layer = np.ones(self.image.data.shape)
            self.cube_images.append(fits.ImageHDU(data=layer, header=self.image.header))
        self.cube = images_to_cube(self.cube_images)
        self.cube.data = np.ones(self.cube.data.shape)

    @pytest.mark.parametrize(('operation'), list([np.sum, np.mean]))
    def test_image(self, operation):
        image_1 = block_reduce_hdu(self.image, (2, 4), func=operation)
        if operation == np.sum:
            ref1 = [[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]]
        if operation == np.mean:
            ref1 = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
        assert_allclose(image_1.data, ref1)

    @pytest.mark.parametrize(('operation'), list([np.sum, np.mean]))
    def test_cube(self, operation):
        for index in self.indices:
            image = cube_to_image(self.cube, index)
            layer = self.cube.data[index]
            layer_hdu = fits.ImageHDU(data=layer, header=image.header)
            image_1 = block_reduce_hdu(layer_hdu, (2, 4), func=operation)
            if operation == np.sum:
                ref1 = [[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]]
            if operation == np.mean:
                ref1 = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
            assert_allclose(image_1.data, ref1)


@requires_dependency('skimage')
def test_ref_pixel():
    image = SkyMap.empty(nxpix=101, nypix=101, proj='CAR')
    footprint = image.wcs.calc_footprint(center=False)
    image_1 = block_reduce_hdu(image.to_image_hdu(), (10, 10), func=np.sum)
    footprint_1 = WCS(image_1.header).calc_footprint(center=False)
    # Lower left corner shouldn't change
    assert_allclose(footprint[0], footprint_1[0])


def test_cube_to_image():
    layer = SkyMap.empty(nxpix=101, nypix=101, fill=1.).to_image_hdu()
    hdu_list = [layer, layer, layer, layer]
    cube = images_to_cube(hdu_list)
    case1 = cube_to_image(cube)
    case2 = cube_to_image(cube, slicepos=1)
    # Check that layers are summed if no layer is specified (case1),
    # or only a specified layer is extracted (case2)
    assert_allclose(case1.data, 4 * layer.data)
    assert_allclose(case2.data, layer.data)


def test_wcs_histogram2d():
    # A simple test case that can by checked by hand:
    header = make_header(nxpix=2, nypix=1, binsz=10, xref=0, yref=0, proj='CAR')
    # GLON pixel edges: (+10, 0, -10)
    # GLAT pixel edges: (-5, +5)

    EPS = 0.1
    data = [
        (5, 5, 1),  # in image[0, 0]
        (0, 0 + EPS, 2),  # in image[1, 0]
        (5, -5 + EPS, 3),  # in image[0, 0]
        (5, 5 + EPS, 99),  # outside image
        (10 + EPS, 0, 99),  # outside image
    ]
    lon, lat, weights = np.array(data).T
    image = wcs_histogram2d(header, lon, lat, weights)

    print(type(image))

    assert image.data[0, 0] == 1 + 3
    assert image.data[0, 1] == 2


@requires_data('gammapy-extra')
def test_lon_lat_rectangle_mask():
    counts = SkyMap.read(FermiGalacticCenter.counts())
    lons, lats = counts.coordinates('galactic')
    mask = lon_lat_rectangle_mask(lons.degree, lats.degree, lon_min=-1,
                                  lon_max=1, lat_min=-1, lat_max=1)
    assert_allclose(mask.sum(), 400)

    mask = lon_lat_rectangle_mask(lons.degree, lats.degree, lon_min=None,
                                  lon_max=None, lat_min=None,
                                  lat_max=None)
    assert_allclose(mask.sum(), 80601)


@requires_data('gammapy-extra')
def test_bin_events_in_cube():
    dirname = '$GAMMAPY_EXTRA/datasets/hess-crab4-hd-hap-prod2'
    data_store = DataStore.from_dir(dirname)

    events = data_store.obs(obs_id=23523).events

    counts = SkyCube.empty(emin=0.5, emax=80, enbins=8, eunit='TeV',
                           nxpix=200, nypix=200, xref=events.meta['RA_OBJ'],
                           yref=events.meta['DEC_OBJ'], dtype='int',
                           coordsys='CEL')
    counts.fill(events)
    assert counts.data.sum().value == 1233



