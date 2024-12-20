cd $GEOIPS_TESTDATA_DIR
ncoda_test_dir=ncoda_test_data/
example_dir=$ncoda_test_dir/example/
static_dir=$ncoda_test_dir/static/

mkdir -p $example_dir
pushd $example_dir
wget https://irma.cira.colostate.edu/index.php/s/23RgTs7JX5ByybW/download/ncoda_ocean_example.zip
unzip ncoda_ocean_example.zip
rm ncoda_ocean_example.zip
popd

mkdir -p $static_dir
pushd $static_dir
wget https://irma.cira.colostate.edu/index.php/s/tH5GDFdK9sZHErH/download/ncoda_static_data.zip
unzip ncoda_static_data.zip
rm ncoda_static_data.zip
popd