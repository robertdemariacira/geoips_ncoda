"""NCODA Algorithm Plugin"""

import logging
from typing import Any, Dict, Optional

import numpy as np
import xarray as xr

from geoips_ncoda.plugins.modules.readers import ncoda_reader

LOG = logging.getLogger(__name__)
MISSING = -999.9

interface = "algorithms"
family = "xarray_dict_to_xarray_dict"
name = "ncoda_algorithm"

TIME_FMT = "%Y-%m-%d-T%H:%M:%SZ"

LAT_ATTRS = {
    "long_name": "latitude",
    "units": "degrees_north",
    "_FillValue": MISSING,
}

LON_ATTRS = {
    "long_name": "longitude",
    "units": "degrees_east",
    "_FillValue": MISSING,
}

ATTRS = {
    "NTDM_GLB_OHC26": {
        "long_name": "NTDM Global Ocean Heat Content 26",
        "units": "K (J/cm^2)",
        "_FillValue": MISSING,
    },
    "NTDM_GLB_SST": {
        "long_name": "NTDM Global Sea Surface Temperature",
        "units": "degC",
        "_FillValue": MISSING,
    },
    "NTDM_GLB_SSS": {
        "long_name": "NTDM Global Sea Surface Temperature",
        "units": "g/kg",
        "_FillValue": MISSING,
    },
    "NTDM_GLB_TD100": {
        "long_name": "NTDM Global depth-avg'd temp assuming constant mixing depth=100m",
        "units": "degC",
        "_FillValue": MISSING,
    },
    "NTDM_GLB_Tdy_c": {
        "long_name": "NTDM Global depth-avg'd temp assuming depth estimated "
        "from constant TC V,max, translational speed, and radius",
        "units": "degC",
        "_FillValue": MISSING,
    },
    "NTDM_GLB_Tdy_p": {
        "long_name": "NTDM Global depth-avg'd temp assuming mixing depth "
        "estimated from  Vmax, and translational speed proxy estimated from GFS",
        "units": "degC",
        "_FillValue": MISSING,
    },
}

LON_NAME = "lon"
LAT_NAME = "lat"
DIMS = (LAT_NAME, LON_NAME)

GLOBAL_ATTRS = {r"Satellite\ Sensor": "DERIVED DATA", "instrument_name": "NTDM_GLB"}


def call(
    xarray_dict: Dict[str, Dict[str, Any]],
    fill_value: Optional[int] = None,
):
    ncoda_ds = xarray_dict[ncoda_reader.GROUP_NAME]
    file_time = ncoda_ds.attrs[ncoda_reader.TIME_ATTR]
    lat_1d = ncoda_ds[ncoda_reader.LAT_NAME].data[0, :]
    lon_1d = ncoda_ds[ncoda_reader.LON_NAME].data[:, 0]

    xr_coords_dict = {LAT_NAME: ([LAT_NAME], lat_1d), LON_NAME: ([LON_NAME], lon_1d)}

    ds_data = {}

    # TODO:Instead of creating empty data, call NCODA library to generate data.
    empty_data = np.zeros((lat_1d.shape[0], lon_1d.shape[0]), dtype=np.float32)

    for var_name, attrs in ATTRS.items():
        var_da = xr.DataArray(
            data=empty_data, dims=DIMS, coords=xr_coords_dict, attrs=attrs
        )
        ds_data[var_name] = var_da

    global_attrs = GLOBAL_ATTRS.copy()
    time_str = file_time.strftime(TIME_FMT)
    global_attrs["date_created"] = time_str
    global_attrs["time_coverage_start"] = time_str
    global_attrs["time_coverage_end"] = time_str
    ncoda_data = xr.Dataset(ds_data, attrs=global_attrs)

    metadata = xarray_dict[ncoda_reader.METADATA_GROUP_NAME]
    return {
        ncoda_reader.GROUP_NAME: ncoda_data,
        ncoda_reader.METADATA_GROUP_NAME: metadata,
    }
