distutils-pytest - Call pytest from a distutils setup.py script
===============================================================

This Python module adds ``test`` to the commands in the `distutils`_
package.  If your ``setup.py`` imports ``distutils_pytest``, the user
may run::

  python setup.py test

This will call `pytest`_ to run your package's test suite.


System requirements
-------------------

 + Python 2.6, 2.7, or 3.1 and newer.
 + `pytest`_

To be honest, the package might also work with older Python versions.
But I didn't try it.


Installation
------------

This package uses the `distutils`_ Python standard library package and
follows its conventions of packaging source distributions.  See the
documentation on `Installing Python Modules`_ for details or to
customize the install process.

  1. Download the sources, unpack, and change into the source
     directory.

  2. Build::

       $ python setup.py build

  3. Install::

       $ python setup.py install

The last step might require admin privileges in order to write into
the site-packages directory of your Python installation.


Copyright and License
---------------------

 - Copyright 2013-2015
   Helmholtz-Zentrum Berlin für Materialien und Energie GmbH
 - Copyright 2015-2016 Rolf Krahl

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _distutils: https://docs.python.org/2.7/library/distutils.html
.. _pytest: http://pytest.org/
.. _Installing Python Modules: https://docs.python.org/2.7/install/
