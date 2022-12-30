"""
***************************************************************************
    constants.py
    ---------------------
    Date                 : December 2022
    Author                : Brendon Hall

Constant definition across field finder module.
***************************************************************************
"""


SPECTRAL_INDICES = ["NDVI"]  # currently implemented spectral indices


ANALYTICMS_8B_INDEX_MAP = (
    {  # band definitions of 8-band PlanetScope OrthoScenes
        "CoastalBlue": 1,
        "Blue": 2,
        "Green1": 3,
        "Green": 4,
        "Yellow": 5,
        "Red": 6,
        "RedEdge": 7,
        "NIR": 8,
    }
)
