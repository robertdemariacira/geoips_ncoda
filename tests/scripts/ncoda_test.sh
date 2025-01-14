# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

# @ Identify and update all instances of @ found within this script appropriately.
# @  @package@ should be the name of this repository
# @ NOTE: imagery_clean preferred to avoid dependencies on external plotting packages
# @       for image consistency,
# @       though you may change the output format if required for your package testing.

# @ Note you may update other arguments within this test call, or add additional
# @ arguments.
# @ Also - the first time you run your test script, it will prompt you to update your
# @ test outputs - at that point you can populate the "tests/outputs" directory,
# @ and your next run will result in a 0 return value.

# @ Please create a separate test script for each piece of functionality you would
# @ like to test.

# @ Ensure each test script is called from the @package@/tests/test_all.sh script.

# @ Point to your desired test data file:
#     $GEOIPS_TESTDATA_DIR/test_data_@datatype@/data/@datafile@ \

# @ Select readername that matches the data file above:
#     --reader_name @readername@ \

# @ Select a product that is available for the above data type
#     --product_name @product@ \

# @ Point to the appropriate comparison directory, where you would like to store your
# @ test outputs. Test output directory name should match the test script name,
# @ by convention.
#     --compare_path "$GEOIPS_PACKAGES_DIR/@package@/tests/outputs/@test_single_source@" \

# @ Modify the 'geoips run single_source' command appropriately for your use case.
# @ Notes above on individual arguments.

    # @ NOTE: --resampled_read argument required for ABI and AHI readers.
    # @ Move into "geoips run single_source" call if using ABI/AHI.
    # --resampled_read \
data_dir=$GEOIPS_TESTDATA_DIR/ncoda_test_data
example_dir=$data_dir/example
static_dir=$data_dir/static

run_procflow \
    $example_dir/salint_pre_000000_005000_1o2161x1051_2023090700_00000000_analfld \
    $example_dir/seatmp_pre_000000_005000_1o2161x1051_2023090700_00000000_analfld \
    $static_dir/grdlat_sfc_000000_000000_1o2161x1051_datafld \
    $static_dir/grdlon_sfc_000000_000000_1o2161x1051_datafld \
    --procflow single_source \
    -l debug \
    --reader_name ncoda_reader \
    --product_name "ncoda_test" \
    --output_formatter ncoda_output \
    --filename_formatter geoips_fname \
    --minimum_coverage 0 \
    --no_presectoring \
    --reader_kwargs '{"source_name": "ncoda"}' \
    --output_formatter_kwargs '{"output_dir":"tests/outputs/ncoda_test/"}'
ss_retval=$?

exit $((ss_retval))
