from typing import Tuple
import numpy as np

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

from .constants import SPECTRAL_INDICES, ANALYTICMS_8B_INDEX_MAP
from .utils import is_valid_geotiff, calculate_ndvi


class SpectralIndex:
    def __init__(self, src_filename, index_type="ndvi") -> None:
        if index_type.upper() in SPECTRAL_INDICES:
            self.index_type = index_type.upper()
            print(f"Creating {self.index_type} spectral index...")
        else:
            raise ValueError(
                f"Spectral index type must be one of {SPECTRAL_INDICES}"
            )

        if not is_valid_geotiff(src_filename):
            raise ValueError(
                f"{src_filename} is not a valid input file for this analysis."
            )

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

    def calculate_index(
        self, src_filename: str, index_type: str
    ) -> Tuple[np.ndarray, dict, tuple]:

        with rasterio.open(src_filename) as src:
            src_meta = src.meta.copy()
            src_bounds = src.bounds

            if index_type == "NDVI":
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
        index = SpectralIndex(input_file, index_type)
        index.write_mask(output_file, threshold=threshold, out_proj=out_proj)
