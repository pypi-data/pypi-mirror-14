# -*- coding: utf-8 -*-

"""
pyyp.exceptions
~~~~~~~~~~~~~~~

This module provides the exceptions for Yunpian.
"""


class RequestException(Exception):
    """Yunpian api exception"""


class Timeout(RequestException):
    """Yunpian api timeout"""


class HTTPError(RequestException):
    """Yunpian api HTTP error"""


class BadResponse(RequestException):
    """Yunpian api bad response error"""
