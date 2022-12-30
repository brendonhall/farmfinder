# -*- coding: utf-8 -*-
"""
***************************************************************************
    spectral_index.py
    ---------------------
    Date                 : December 2022
    Author                : Brendon Hall

Model for creating and managing spectral indices.
***************************************************************************
"""
__author__ = "Brendon Hall"
__date__ = "December 2022"


from typing import Tuple
import numpy as np

import warnings


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

from .constants import SPECTRAL_INDICES, ANALYTICMS_8B_INDEX_MAP
from .utils import is_valid_geotiff, calculate_ndvi


class SpectralIndex:
    """This is the main model class for creating a spectral index from an
    8-band PlanetScope OrthoScene.

    SpectralIndex objects can be created in two ways: with just a filename and
    with a filename and an xml metadata file.

    Attributes
    ----------
    index_type : str
        string indicating the name of the spectral index (NDVI is default)
    values : np.ndarray (2d)
        2d array that holds the values of the calculated spectral index.
    src_meta : dict
        Meta-data from the source GeoTiff file.
    src_bounds : tuple
        Spatial bounds of the source GeoTiff file.
    src_filename: str
        Filename of the source GeoTiff image

    Methods
    -------
    get_mask() - get the mask based on the index values and a given
                 threshold
    write_mask() - write a mask based the index values and a threshold
                   to a file, reprojecting if needed.

    Public Static methods
    ---------------------
    create_mask_file() - helper function to create a mask file based on an
                         index from a geotiff.  Output file will be reprojected
                         if necessary.
    """

    def __init__(self, src_filename, index_type="ndvi") -> None:
        """
        Create a spectral index based on a source GeoTiff file.  Note that this
        constructor will use the raw DNs in the GeoTiff file.  For
        PlanetScope OrthoScene images, these will be radiance values.  This
        may be appropriate for an analysis of a single image. If analysis
        across a series of images is to be performed, these values should be
        converted to TOA reflectance using coefficients in the metadata that
        accompanies the TIF files.

        :param src_filename: filename of the source image.
        :type dst_filename: str
        :param index_type: spectral index name to calculate, defaults to 'NDVI'
        :type index_type: str, optional
        """
        if index_type.upper() in SPECTRAL_INDICES:
            self.index_type = index_type.upper()
            print(f"Creating {self.index_type} spectral index...")
        else:
            raise ValueError(
                f"Spectral index type must be one of {SPECTRAL_INDICES}"
            )

        # For now, just ensure source image has 8 bands
        if not is_valid_geotiff(src_filename):
            raise ValueError(
                f"{src_filename} is not a valid input file for this analysis."
            )
        else:
            self.src_filename = src_filename

        self.values, self.src_meta, self.src_bounds = self.calculate_index(
            src_filename, self.index_type
        )

    def get_mask(self, threshold: float = 0) -> np.ndarray:
        """
        Generate a binary mask based on the spectral index values.  Mask
        pixels will be 255 if the spectral index values are greater than the
        threshold parameter, and 0 otherwise.

        :param threshold: index threshold values, defaults to 0
        :type threshold: float, optional
        :return: binary mask of the spectral index.
        :rtype: np.ndarry
        """

        min_value = self.values.min()
        max_value = self.values.max()

        if threshold < min_value or threshold > max_value:
            warnings.warn(
                f"Threshold value of {threshold} is outside the range of the \
                  index values."
            )

        masked_index = np.where(self.values >= threshold, 255, 0)
        masked_index = masked_index.astype(np.uint8)

        return masked_index

    def write_mask(
        self, dst_filename: str, threshold: float = None, out_proj: str = None
    ) -> None:
        """
        Generate an image mask of the index based on threshold.  Reproject if
        necessary.

        :param dst_filename: filename of the destination image.
        :type dst_filename: str
        :param threshold: index value cutoff, defaults to None
        :type threshold: float, optional
        :param out_proj: CRS to reproject to, defaults to None
        :type out_proj: str, optional
        """

        # handle the case were there is no out_proj (don't need to reproject)

        transform, width, height = calculate_default_transform(
            self.src_meta["crs"],
            out_proj,
            self.src_meta["width"],
            self.src_meta["height"],
            *self.src_bounds,
        )

        dst_meta = self.src_meta.copy()

        dst_meta.update(
            {
                "crs": out_proj,
                "transform": transform,
                "width": width,
                "height": height,
                "count": 1,
                "dtype": "uint8",
                "nodata": 0,
            }
        )

        masked_index = self.get_mask(threshold)

        with rasterio.open(dst_filename, "w", **dst_meta) as dst:

            reproject(
                source=masked_index,
                destination=rasterio.band(dst, 1),
                src_transform=self.src_meta["transform"],
                src_crs=self.src_meta["crs"],
                dst_transform=transform,
                out_proj=out_proj,
                resampling=Resampling.nearest,
            )

    def calculate_index(self) -> Tuple[np.ndarray, dict, tuple]:
        """Private method to read src_geotiff file, extract meta data and
           compute the relevant spectral index.

        :return: Tuple with index array, source meta data and source bounds
        :rtype: Tuple(np.ndarray, dict, tuple)
        """

        with rasterio.open(self.src_filename) as src:
            src_meta = src.meta.copy()
            src_bounds = src.bounds

            if self.index_type == "NDVI":
                red = src.read(ANALYTICMS_8B_INDEX_MAP["Red"])
                nir = src.read(ANALYTICMS_8B_INDEX_MAP["NIR"])

                ndvi = calculate_ndvi(red=red, nir=nir)

                return ndvi, src_meta, src_bounds

    @staticmethod
    def create_mask_file(
        input_file: str,
        output_file: str,
        threshold: float = 0,
        out_proj: str = None,
        index_type: str = "ndvi",
    ):
        """Helper function to write a spectral index mask file and reproject
        in one step.

        :param input_file: Source 8-band PlanetScope OrthoScene Geotiff.
        :type input_file: str
        :param output_file: Destination geotiff file to store the mask file.
        :type output_file: str
        :param threshold: Threshold value for identifying index mask cutoff,
                          defaults to 0
        :type threshold: float, optional
        :param out_proj: Output projection CRS, in EPSG code format,
                         defaults to None if no reprojection necessary
        :type out_proj: str, optional
        :param index_type: Spectral Index to calculate, defaults to "ndvi"
        :type index_type: str, optional
        """
        index = SpectralIndex(input_file, index_type)
        index.write_mask(output_file, threshold=threshold, out_proj=out_proj)
