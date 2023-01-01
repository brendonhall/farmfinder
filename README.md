![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/brendonhall/fieldfinder)
[![Code Coverage](https://img.shields.io/codecov/c/github/brendonhall/fieldfinder)](https://codecov.io/github/brendonhall/fieldfinder)

# FieldFinder

Fieldfinder is a Python module for detecting agricultural development in 8-band PlanetScope images.  Information about land cover can be extracted from the different wavelength bands in a multispectral image.  Spectral Indices are combinations and ratios of the different bands, and can be used as features to identify land coverage.  A common index for identifying vegetation is the normalized difference vegetation index (NDVI).  The measure scales with the presence of live, green vegetation.  The formula for NDVI is:
$$NDVI = \frac{NIR - R}{NIR + R}$$
NDVI is the ratio of the difference of the red (R) and near-infrared (NIR) radiances over their sum as a means to adjust for or “normalize” the effects of the solar zenith angle.  Live green plants appear relatively dark in the photosynthetically active radiation (PAR) band and relatively bright in the near-infrared.  Thus high values of NDVI would indicate dense vegetation (ie: agriculture).

**Note:** There are many spectral indices besides NDVI ([Agapiou 2012](https://static1.1.sqspcdn.com/static/f/891472/21277561/1355603890193/Agapiou_et_al._2012.pdf)),
and `fieldfinder` can be easily expanded to accomodate these.

### Radiance vs. Reflectance
Planet Labs' analytic data products are [reported in units of radiance](https://notebook.community/planetlabs/notebooks/jupyter-notebooks/toar/toar_planetscope): $W*m^{-2}*sr^{-1}$.  This quantifies the amount of light captured over a given spot on the ground.  This depends on the amount and frequencies of light that are reflected from the surface, but also on satellite altitude, time of day, time of year and individual satellite characteristics.  To compare spectral indices across many images, radiance values should be converted to Top of Atmosphere (TOA) reflectance to provide an `apples-to-apples` comparison 

## Installation

    pip install fieldfinder

## Quickstart
`fieldfinder` is designed to calculate a spectral index (such as NDVI) from an 8-band PlanetScope AnalyticMS image, and output a raster mask that indicates where the mask exceeds a given threshold.  The following example demonstrates how to create an NVDI spectral index from an 8-band PlanetScope image, and output a mask file with values of 255 where NDVI > 0.65, and zero otherwise.  The output file is reprojected to lat/long (EPSG:4326) coordinates.

```python
from fieldfinder import SpectralIndex

SpectralIndex.create_mask_file(
    filename = 'example_AnalyticMS_8b.tif',
    output_file = 'example_NDVI_mask.tif',
    threshold=0.65,
    out_proj = 'EPSG:4326',
    index_type = 'ndvi'
)
```