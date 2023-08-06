from __future__ import print_function
import os.path

def test_import():
    """Check that importing the module works.
    """
    import distutils_pytest
    modpath = os.path.dirname(os.path.abspath(distutils_pytest.__file__))
    print("version: %s" % distutils_pytest.__version__)
    print("module path: %s" % modpath)
