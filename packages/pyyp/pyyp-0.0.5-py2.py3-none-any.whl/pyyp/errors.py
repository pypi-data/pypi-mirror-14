# -*- coding: utf-8 -*-

"""
pyyp.errors
~~~~~~~~

This module provides the errors for Yunpian.
"""


class YunpianError(Exception):
    """Yunpian api error"""


class YunpianTransportError(Exception):
    """Yunpian api transport error"""


class YunpianBadResponse(Exception):
    """Yunpian api bad response error"""
