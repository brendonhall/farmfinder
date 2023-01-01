"""
***************************************************************************
    utils.py
    ---------------------
    Date                 : December 2022
    Author                : Brendon Hall

Utility and helper functions for field finder module.
***************************************************************************
"""
__author__ = "Brendon Hall"
__date__ = "December 2022"

import numpy as np

import rasterio

from .constants import ANALYTICMS_8B_INDEX_MAP


def is_valid_geotiff(src_filename: str) -> bool:
    """
    Validation method to ensure src_geotiff is a valid 8 band AnalyticMS image.
    Keep this simple for now - just check to see if the image has the
    appropriate number of bands.

    :param src_filename: filename of the src geotiff
    :type src_filename: str
    """
    with rasterio.open(src_filename) as src:
        num_bands = src.meta["count"]
        if num_bands != len(ANALYTICMS_8B_INDEX_MAP):
            raise ValueError(
                f"{src_filename} is not a valid 8-band source image."
            )

    return True


def calculate_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """Calculate ndvi accoring to the formula
        ndvi = (nir-red) / (nir + red)

    See https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
    for reference.

    :param red: 2d numpy array of red image values
    :type red: np.ndarray
    :param nir: 2d numpy array of nir image values
    :type nir: np.ndarray
    :return: 2d array of calculated ndvi values
    :rtype: np.ndarray
    """

    # Allow division by zero
    np.seterr(divide="ignore", invalid="ignore")

    ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)

    return ndvi
