# main file for classes to be used.
import argparse

from .spectral_index import SpectralIndex


parser = argparse.ArgumentParser(
    description="Create an agriculture mask from a PlanetScope \
                 Ortho scene based on a spectral index (ie: NDVI) and \
                 a given threshold."
)

parser.add_argument(
    "-s",
    "--src",
    help="Source 8-band PlanetScope Ortho Scence GeoTiff image.",
)

parser.add_argument(
    "-o",
    "--output",
    help="Output GeoTiff image for spectral index mask.",
)

parser.add_argument(
    "--p",
    "--proj",
    help="CRS for projection of output file.",
)

parser.add_argument(
    "--t",
    "--threshold",
    help="Threshold for creating the spectral index mask.",
)

args = parser.parse_args()

script_params = {}

if args.file:
    pass
    # logger.info(f"Reading parameter file {args.file.name}")
    # script_params = json.load(args.file)

if args.viz:
    script_params["build_dashboard"] = True
if args.save:
    script_params["save_models"] = True


def write_NDVI_mask(
    input_file: str,
    output_file: str,
    threshold: float = 0,
    out_proj: str = None,
):

    ndvi = SpectralIndex(input_file)
    ndvi.write_mask(output_file, threshold=threshold, out_proj=out_proj)
