# TODO: Switch to python-behave
cd ../
python setup.py install
cd -
pybot -o report/output.xml -l report/log.html -r report/index.html -N "Cinder Data" suites/*
