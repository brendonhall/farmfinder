# import numpy as np
# import logging

import os
from pathlib import Path

import pytest


# LOGGER = logging.getLogger(__name__)

_here = Path(os.path.abspath(os.path.dirname(__file__)))
_test_data_path = _here / "data"


@pytest.fixture
def open_test_img():
    img_path = _test_data_path / "test_sm.tif"
    with open(img_path, "rb") as img:
        yield img


def test_NDVA_extractor():
    assert True == True


@pytest.mark.parametrize(
    "test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)]
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected


def test_img_read(open_test_img):
    img = open_test_img
