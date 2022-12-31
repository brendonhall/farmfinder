![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/brendonhall/fieldfinder)
[![Code Coverage](https://img.shields.io/codecov/c/github/brendonhall/fieldfinder)](https://codecov.io/github/brendonhall/fieldfinder)

# FieldFinder

Fieldfinder is a Python module for detecting agricultural development in 8-band PlanetScope images.  Information about land cover can be extracted from the different wavelength bands in a multispectral image.  Spectral Indices are combinations and ratios of the different bands, and can be used as features to identify land coverage.  A common index for identifying vegetation is the normalized difference vegetation index (NDVI).  The measure scales with the presence of live, green vegetation.  The formula for NDVI is:
$$NDVI = \frac{NIR - R}{NIR + R}$$
NDVI is the ratio of the difference of the red (R) and near-infrared (NIR) radiances over their sum as a means to adjust for or “normalize” the effects of the solar zenith angle.  Live green plants appear relatively dark in the photosynthetically active radiation (PAR) band and relatively bright in the near-infrared.  Thus high values of NDVI would indicate dense vegetation (ie: agriculture).

**Note:** There are many spectral indices besides NDVI ([Agapiou 2012](https://static1.1.sqspcdn.com/static/f/891472/21277561/1355603890193/Agapiou_et_al._2012.pdf)),
and `fieldfinder` can be easily expanded to accomodate these.


## Installation

    pip install fieldfinder

## Quickstart

### Coding Task
#### Geospatial Software Engineer

Your task is to write a rudimentary agricultural field detector. Do this by calculating NDVI for a given 8-band image. NDVI values will be high where there are plants and lower where they are
absent.

- Given an 8-band geotiff in UTM projection, calculate NDVI and output a geotiff one in Lat/Long (EPSG 4326) projection.
- Pixels in output images should have a value of 255 where fields are located and 0 elsewhere.
- Code must be written as a Python module.
- Provide
    - internal and external documentation
    - instructions for use including environment setup and sample code
- Code must allow client code to specify the threshold for determining which NDVI values should be considered as part of a field.

Bonus Points:
- Tests
- Ease of setup
The code does not need to find the fields perfectly. There will likely be some false positives and
false negatives.

Sample Data:
[https://hello.planet.com/data/s/L6GYNf4N6wTRydD](https://hello.planet.com/data/s/L6GYNf4N6wTRydD)

Helpful Info:
[NDVI Wikipedia Page](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index)

NDVI = (NIR - R) / (NIR + R)
NIR = Near Infrared
R = Red

Band order in given image:
- Band 1: Coastal Blue
- Band 2: Blue
- Band 3: Green I
- Band 4: Green
- Band 5: Yellow
- Band 6: Red
- Band 7: Red Edge
- Band 8: Near Infrared (NIR)
 
----------------------
**NDVI**
The normalized difference vegetation index (NDVI) is a simple vegatation indicator that can be calculated from satellite imagery.  The measure scales with the presence of live, green vegetation.

- ratio of the difference of the red and infrared radiances over their sum as a means to adjust for or “normalize” the effects of the solar zenith angle.
- most well-known and used index to detect live green plant canopies in multispectral remote sensing data. 
-  live green plants appear relatively dark in the PAR and relatively bright in the near-infrared.

The formula to calculate $NDVI$ is:

$$NDVI = \frac{NIR - R}{NIR + R}$$

where $R$ and $NIR$ stand for the spectral reflectance measurements acquired in the red (visible) and near-infrared regions, respectively.

#### Ideas
- smoothing with CRF, clean up isolated pixels/holes