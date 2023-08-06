# SiQt

[![Build Status](https://travis-ci.org/rth/SiQt.svg?branch=master)](https://travis-ci.org/rth/SiQt)


A compatibility library for PyQt4, PyQt5 and PySide.

*Warning: This is a pre-alpha version that should not be used in production. Backward compatibility is not guaranteed at this point.*


## Installation

 This package requires Python 2.7 or 3.2-3.5 with `six` and one of the following backends: `PyQt4`, `PySide`, `PyQt5`.

 It can be installed with, 
    
    pip install git+https://github.com/rth/SiQt.git

## Quick start
 
 Assuming you have GUI script `my_pyqt4_gui.py` written with PyQt4 (or any other backend), you can attempt to run it with PySide (or any other backend) using,

    SIQT_BACKEND_FORCE='PySide' python -m SiQt my_pyqt4_gui.py

*Note that the compatibility hooks are still being actively developped and this may fail due to API differences* 

## Functionality

 SiQt provides a layer of bstraction to work with the existing Python Qt libraries.


#### 1. Aliasing
 
 The SiQt package will redirect imports to the active PyQt/PySide backend:

    import SiQt
    SiQt.use('PyQt4') 

    from SiQt import QtCore, Qt # or any other module that would be imported from PyQt4

#### 2. Import interception

 With the `force=True` option, imports of PyQt4, PyQt5, PySide can be intercepted to load SiQt instead, which itself
redirects to the active PyQt/PySide backend:
  

    import SiQt
    SiQt.use('PyQt5', force=True)

    import PyQt4
    import PyQt4.QtCore

    print(PyQt4.__name__)              # SiQt
    print(SiQt.backend)                # PyQt5
    print(PyQt4.QtCore.QT_VERSION_STR) # 5.5.1


#### 3. Compatibility layer

 By default, `SiQt.use` is called with the `mode='compatible'` argument, which attempts to compensate the differences in the API
 between backends (*in developpement*). Alternatively, one can set `mode='strict'` to avoid this behaviour.

## Command line use
 
 Most of the SiQt functionality is accessible through command line, where the `SiQt.use` arguments can be passed as environment variables:

   - `SIQT_BACKEND='name'` is equivalent to `SiQt.use('name', force=False)`
   - `SIQT_BACKEND_FORCE='name'` is equivalent to `SiQt.use('name', force=True)`
   - `SIQT_MODE='name'` is equivalent to `SiQt.use(..., mode='mode')`


SiQt can be enabled on any script without changing its source code with,

    SIQT_BACKEND_FORCE='name' python -m SiQt  original_script.py

## Unit tests

 The test suite can be run with,
 
    python -c "from SiQt.siqt import tests; tests.run()"
