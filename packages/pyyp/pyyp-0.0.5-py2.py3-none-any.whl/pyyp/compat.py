# -*- coding: utf-8 -*-

"""
pyyp.compat
~~~~~~~~~~~

This module provides some python 2 and python 3 compatibility.
"""

import sys

_ver = sys.version_info

is_py2 = (_ver[0] == 2)

is_py3 = (_ver[0] == 3)
