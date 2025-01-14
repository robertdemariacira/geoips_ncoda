"""NCODA reader plugin."""

import datetime as dt
import logging
import pathlib
import re
from typing import Dict, List, Optional

import pyresample
import xarray as xr
from ncoda_util import reader

log = logging.getLogger(__name__)

interface = "readers"
family = "standard"
name = "ncoda_reader"

LON_NAME = "longitude"
LAT_NAME = "latitude"

# Maps filename prefixes to variable names
PREFIX_TO_VAR_MAP = {
    "seatmp": "sst",
    "salint": "salinity",
}

PREFIX_TO_COORD_MAP = {"grdlon": LON_NAME, "grdlat": LAT_NAME}

DIMENSIONS_2D = ["x", "y"]
DIMENSIONS_3D = ["x", "y", "z"]

GROUP_NAME = "ncoda"
METADATA_GROUP_NAME = "METADATA"

DEFAULT_TIME_REGEX = r"\w+(?P<time>_\d{10}_\d{4})\d+\w+$"
DEFAULT_TIME_FORMAT = "_%Y%m%d%H_%M%S"

TIME_ATTR = "time"


def call(
    fnames: List[str],
    source_name: str,
    metadata_only: bool = False,
    chans: Optional[List[str]] = None,
    area_def: Optional[pyresample.geometry.AreaDefinition] = None,
    self_register: bool = False,
    prefix_to_var_map: Dict[str, str] = PREFIX_TO_VAR_MAP,
    prefix_to_coord_map: Dict[str, str] = PREFIX_TO_COORD_MAP,
    time_regex: str = DEFAULT_TIME_REGEX,
    time_format: str = DEFAULT_TIME_FORMAT,
) -> Dict[str, xr.Dataset]:
    """Reads NCODA ocean data.

    Args:
        fnames (List[str]): List of filenames.
        source_name (str): GeoIPS source name.
        metadata_only (bool, optional): Required by GeoIPS, currently unused.
            Defaults to False.
        chans (Optional[List[str]], optional): Required by GeoIPS, currently
            unused. Defaults to None.
        area_def (Optional[pyresample.geometry.AreaDefinition], optional):
            Required by GeoIPS, currently unused. Defaults to None.
        self_register (bool, optional): Required by GeoIPS, currently unused.
            Defaults to False.
        prefix_to_var_map (Dict[str, str], optional): Maps file prefixes to the
            variable the file contains. Defaults to PREFIX_TO_VAR_MAP.
        prefix_to_coord_map (Dict[str, str], optional): Maps file prefixes to
            the coordinate the file contains. Defaults to PREFIX_TO_COORD_MAP.
        time_regex (str, optional): Regular expression used to extract time
            information from a filename. Must provied a named capture group
            called "time". Defaults to DEFAULT_TIME_REGEX.
        time_format (str, optional): The strftime format to use to extract time
            from the "time" named capture group found by the time_regex.
            Defaults to DEFAULT_TIME_FORMAT.

    Raises:
        ValueError: If no files are found that can be used to extract time
        information from.

    Returns:
        Dict[str, xr.Dataset]: GeoIPS reader plugin dictionary of Datasets.
    """
    paths = [pathlib.Path(f) for f in fnames]
    vars_to_paths = _make_var_to_path_map(paths, prefix_to_var_map)
    coords_to_paths = _make_var_to_path_map(paths, prefix_to_coord_map)

    coord_data = {}
    for coord_name, coord_path in coords_to_paths.items():
        coord_array = reader.read_coord(coord_path)
        coord_data[coord_name] = coord_array
    lons = coord_data[LON_NAME]
    lats = coord_data[LAT_NAME]
    xr_coords_dict = {LON_NAME: (DIMENSIONS_2D, lons), LAT_NAME: (DIMENSIONS_2D, lats)}

    var_data = {}
    file_time = None
    for var_name, var_path in vars_to_paths.items():
        var_array = reader.read_data(var_path)
        var_da = xr.DataArray(data=var_array, dims=DIMENSIONS_3D, coords=xr_coords_dict)

        var_data[var_name] = var_da

        if file_time is None:
            file_time = _extract_time(var_path, time_regex, time_format)

    if file_time is None:
        raise ValueError("Could not find any files to extract time from.")

    attrs = {
        "source_name": source_name,
        TIME_ATTR: file_time,
        "start_datetime": file_time,
        "end_datetime": file_time,
    }

    out_ds = xr.Dataset(var_data, attrs=attrs)
    datasets = {GROUP_NAME: out_ds, METADATA_GROUP_NAME: out_ds[[]]}

    return datasets


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


def _extract_time(
    filename: pathlib.Path, time_regex: str, time_format: str
) -> dt.datetime:
    regex = re.compile(time_regex)

    m = regex.search(filename.name)
    if m is None:
        raise ValueError(f"Could not match regex: {time_regex} to filename: {filename}")

    time_str = m.groupdict()["time"]
    time = dt.datetime.strptime(time_str, time_format)

    return time
