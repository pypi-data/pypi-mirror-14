#!/bin/bash
set -x

if [[ $SIQT_BACKEND == 'PyQt4' ]]; then 
        conda install --yes "PyQT=4.11"
elif [[ $SIQT_BACKEND == 'PyQt5' ]]; then 
    if [[ $TRAVIS_PYTHON_VERSION == "3.4" ]]; then
        conda install -c https://conda.anaconda.org/dsdale4 pyqt5
    else  # Python 3.5 or 2.7
        conda install --yes -c https://conda.anaconda.org/spyder-ide pyqt5
    fi
elif  [[ $SIQT_BACKEND == 'PySide' ]]; then
    if [[ ${TRAVIS_PYTHON_VERSION:0:1} == 2 ]]; then
        conda install --yes "pyside"
    else
        conda install --yes -c pyzo pyside-pyzo
    fi
fi
