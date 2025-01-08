"""Output formatter plugin to write data as AWIPS compatible netCDF tiles."""

import logging

import xarray as xr

LOG = logging.getLogger(__name__)

interface = "output_formatters"
family = "xrdict_to_outlist"
name = "ncoda_output"


def call(xarray_obj: xr.Dataset):
    # wrtie stuff here
    breakpoint()
    return ["foo"]
