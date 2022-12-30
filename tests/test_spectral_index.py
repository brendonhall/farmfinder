import numpy as np

import logging

import os
from pathlib import Path

import pytest

from fieldfinder.spectral_index import SpectralIndex

logger = logging.getLogger(__name__)

TEST_INPUT_GEOTIFF = "test_AnalyticMS_8b.tif"

_here = Path(os.path.abspath(os.path.dirname(__file__)))
_test_data_path = _here / "data"

red_band_test = np.array(
    [
        [2994, 3021, 3014, 2996, 2975],
        [2970, 2972, 2975, 2984, 3022],
        [3006, 2992, 2965, 2960, 3005],
        [3019, 2974, 2927, 2905, 2911],
        [2976, 2922, 2861, 2844, 2864],
    ],
    dtype=np.uint16,
)

nir_band_test = np.array(
    [
        [6443, 6496, 6574, 6665, 6735],
        [6532, 6582, 6572, 6589, 6614],
        [6626, 6632, 6591, 6553, 6523],
        [6639, 6676, 6639, 6572, 6515],
        [6546, 6634, 6655, 6641, 6610],
    ],
    dtype=np.uint16,
)

ndvi_values_test = np.array(
    [
        [0.36547632, 0.36513607, 0.37129746, 0.37977435, 0.38722966],
        [0.37486845, 0.37785221, 0.37676757, 0.37657996, 0.37276878],
        [0.37583056, 0.37822111, 0.37944747, 0.37769368, 0.36922754],
        [0.3748188, 0.38362694, 0.38804098, 0.38693679, 0.3823467],
        [0.37492124, 0.38844705, 0.39869693, 0.40031629, 0.39539793],
    ]
)

ndvi_mask_0_65_test = np.array(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
)

ndvi_mask_0_38_test = np.array(
    [
        [0, 0, 0, 0, 255],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 255, 255, 255, 255],
        [0, 255, 255, 255, 255],
    ]
)


def test_file_constructor_type():
    img_path = _test_data_path / TEST_INPUT_GEOTIFF
    index = SpectralIndex(img_path)
    assert isinstance(index, SpectralIndex)


def test_file_constructor_values():
    img_path = _test_data_path / TEST_INPUT_GEOTIFF
    index = SpectralIndex(img_path)
    np.testing.assert_array_almost_equal(index.values, ndvi_values_test)


def test_mask_065():
    img_path = _test_data_path / TEST_INPUT_GEOTIFF
    index = SpectralIndex(img_path)
    mask = index.get_mask(threshold=0.65)
    np.testing.assert_array_equal(mask, ndvi_mask_0_65_test)


def test_mask_036():
    img_path = _test_data_path / TEST_INPUT_GEOTIFF
    index = SpectralIndex(img_path)
    mask = index.get_mask(threshold=0.38)
    np.testing.assert_array_equal(mask, ndvi_mask_0_38_test)
