"""Output formatter plugin to write data as AWIPS compatible netCDF tiles."""

import logging
import pathlib
from typing import Any, Dict, List, Union

import xarray as xr

from geoips_ncoda.plugins.modules.readers import ncoda_reader

LOG = logging.getLogger(__name__)

interface = "output_formatters"
family = "xrdict_to_outlist"
name = "ncoda_output"

DEFAULT_FILENAME_FORMAT = "A2NCGRD_NTDM_GLB_{start_time:%Y%m%d}_{start_time:%H%M}.nc"


def call(
    xarray_obj: Dict[str, xr.Dataset],
    output_dir: str,
    filename_format: str = DEFAULT_FILENAME_FORMAT,
) -> List[str]:
    metadata = xarray_obj[ncoda_reader.METADATA_GROUP_NAME]
    start_datetime = metadata.attrs["start_datetime"]

    out_filename = filename_format.format(start_time=start_datetime)
    full_path = pathlib.Path(output_dir, out_filename)

    ds = xarray_obj[ncoda_reader.GROUP_NAME]
    ds.to_netcdf(full_path)
    return [str(full_path)]
