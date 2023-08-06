import os

# Make sure the user points to a MuJoCo binary installation.
try:
    bundle_path = os.environ['MUJOCO_PY_BUNDLE_PATH']
except KeyError:
    raise RuntimeError("Please set a MUJOCO_PY_BUNDLE_PATH variable to point to your MuJoCo binary bundle. (It should have a key.txt at the top-level, and linux/osx/win directories containing the relevant unpacked binaries.)")

from .mjviewer import MjViewer
from .mjcore import MjModel
from .mjcore import register_license
import os
import sys
from mjconstants import *
from platname_targdir import targdir

register_license(os.path.join(bundle_path, "key.txt"))
