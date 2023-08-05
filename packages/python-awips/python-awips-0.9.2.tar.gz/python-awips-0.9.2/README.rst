Python Data Access Framework for AWIPS II
=========================================

|PyPi| |PyDownloads|

.. |PyPI| image:: https://img.shields.io/pypi/v/python-awips.svg
       :target: https://pypi.python.org/pypi/python-awips/
    :alt: PyPI Package

.. |PyPIDownloads| image:: https://img.shields.io/pypi/dm/python-awips.svg
       :target: https://pypi.python.org/pypi/python-awips/
    :alt: PyPI Downloads



The `dateutil` module provides powerful extensions to
the standard `datetime` module, available in Python.



### Install Requirements

* easy_install argparse
* easy_install shapely
* yum install geos geos-devel (or "brew install goes" for OS X)

### Install

## pip

	pip install python-awips

## github

* git clone https://github.com/Unidata/python-awips.git
* cd python-awips
* python setup.py install

### Install for AWIPS II

	wget https://bootstrap.pypa.io/ez_setup.py -O - | /awips2/python/bin/python
	easy_install pip
	/awips2/python/bin/pip install python-awips
