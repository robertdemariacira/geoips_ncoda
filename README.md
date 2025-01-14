    # # # This source code is protected under the license referenced at
    # # # https://github.com/NRLMMD-GEOIPS.

# geoips_ncoda

Provides GeoIPS plugins for working with NCODA Ocean Data and producing AWIPS
compatible netCDF files.

Three plugins are provided:
- `geoips_ncoda.plugins.modules.readers.ncoda_reader`:
    - Reads NCODA data and outputs the standard GeoIPS dictionary of Datasets.
- `geoips_ncoda.plugins.modules.algorithms.ncoda_algorithm`:
    - Uses data read from the NCODA reader plugin, runs the NCODA algorithm to
        produce the following six variables: `NTDM_GLB_OHC26, NTDM_GLB_SST, NTDM_GLB_SSS, NTDM_GLB_TD100, NTDM_GLB_Tdy_c, NTDM_GLB_Tdy_p`.
    - WARNING: Currently this will exclusively produce missing data and the 
        current code is intended to be a placeholder until this functionality is
        implemented.
- `geoips_ncoda.plugins.modules.output_formatters.ncoda_output`:
    - Assumes that input is coming from the `ncoda_algorithm` plugin and writes
        an AWIPS compatible netCDF file from the data.

## Test Case
A test case is provided to demonstrate usage and verify output is produced correctly.
The test case assumes that the `tests/scripts/get_test_data.sh` script has been run
to obtain the data the test uses.

The test case can be run from the repo root using the command: 
`tests/scripts/ncoda_test.sh`.

This will create the following AWIPS compatible netCDF file: 
`tests/outputs/ncoda_test/A2NCGRD_NTDM_GLB_20230907_0000.nc`
