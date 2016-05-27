cd ../
python setup.py install
cd -
sphinx-apidoc -o source ../cinder_data
make html
