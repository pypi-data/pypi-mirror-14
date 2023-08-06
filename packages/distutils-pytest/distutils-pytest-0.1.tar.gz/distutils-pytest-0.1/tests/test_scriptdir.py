from __future__ import print_function
import os

def test_scriptdir():
    """Check that BUILD_SCRIPTS_DIR is set.
    """
    script_dir = os.environ['BUILD_SCRIPTS_DIR']
    assert script_dir
    print("script_dir: %s" % script_dir)
