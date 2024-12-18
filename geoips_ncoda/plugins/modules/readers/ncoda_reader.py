import logging
import pathlib
from typing import Dict, List, Optional

import pyresample
import xarray as xr
from ncoda_util import reader

log = logging.getLogger(__name__)

interface = "readers"
family = "standard"
name = "ncoda_reader"

# Maps filename prefixes to variable names
PREFIX_TO_VAR_MAP = {
    "seatmp": "sst",
    "seahgt": "sea_height",
    "salint": "salinity",
}

PREFIX_TO_COORD_MAP = {"grdlon": "longitude", "grdlat": "latitude"}


def call(
    fnames: List[str],
    metadata_only: bool = False,
    chans: Optional[List[str]] = None,
    area_def: Optional[pyresample.geometry.AreaDefinition] = None,
    self_register: bool = False,
    prefix_to_var_map: Dict[str, str] = PREFIX_TO_VAR_MAP,
    prefix_to_coord_map: Dict[str, str] = PREFIX_TO_COORD_MAP,
) -> Dict[str, xr.DataArray]:
    paths = [pathlib.Path(f) for f in fnames]
    vars_to_paths = _make_var_to_path_map(paths, prefix_to_var_map)
    coords_to_paths = _make_var_to_path_map(paths, prefix_to_coord_map)

    coord_data = {}
    for coord_name, coord_path in coords_to_paths.items():
        coord_array = reader.read_coord(coord_path)
        coord_data[coord_name] = coord_array

    var_data = {}
    for var_name, var_path in vars_to_paths.items():
        var_array = reader.read_data(var_path)
        var_data[var_name] = var_array

    out_ds = xr.Dataset(var_data, coords=coord_data)


def _make_var_to_path_map(
    paths: List[pathlib.Path], prefix_to_var_map: Dict[str, str]
) -> Dict[str, pathlib.Path]:
    var_to_path_map = {}
    for prefix, var in prefix_to_var_map.items():
        for p in paths:
            if p.name.startswith(prefix):
                var_to_path_map[var] = p
                break

    return var_to_path_map
