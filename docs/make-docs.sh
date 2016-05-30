cd ../
python setup.py install
cd -
rm -rf source/*
sphinx-apidoc --separate -o source ../cinder_data
make html
