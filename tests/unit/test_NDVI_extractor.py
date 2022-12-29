import numpy as np
import logging

import os
from pathlib import Path

import pytest

from fieldfinder.NDVI_extractor import ndva_from_values


LOGGER = logging.getLogger(__name__)

_here = Path(os.path.abspath(os.path.dirname(__file__)))
_test_data_path = _here / "data"


@pytest.fixture
def open_test_img():
    img_path = _test_data_path / "test_sm.tif"
    with open(img_path, "rb") as img:
        yield img


def test_NDVA_extractor():
    a = 1
    assert a == 1


@pytest.mark.parametrize(
    "test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)]
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected


def test_img_read(open_test_img):
    img = open_test_img
    assert isinstance(img, object)


def test_ndva_from_values():
    assert ndva_from_values(1, 3) == 0.5


def test_ndva_from_vector():
    red_vec = np.array([1, 1])
    infred_vec = np.array([3, 3])
    np.testing.assert_array_equal(
        ndva_from_values(red_vec, infred_vec), np.array([0.5, 0.5])
    )
