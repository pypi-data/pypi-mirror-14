# -*- coding: utf-8 -*-

"""
pyyp.client
~~~~~~~~~~~

This module provides the http client for Yunpian.
"""

import requests

from .errors import YunpianTransportError


class Client(object):
    """Client to send requests"""

    def __init__(self, timeout):
        self._session = requests.session()
        self._timeout = timeout

    def get(self, request):
        try:
            return self._get(request)
        except requests.exceptions.RequestException as e:
            raise YunpianTransportError(e)

    def _get(self, request):
        return self._session.get(request.uri,
                                 params=request.params,
                                 timeout=self._timeout)

    def post(self, request):
        try:
            return self._post(request)
        except requests.exceptions.RequestException as e:
            raise YunpianTransportError(e)

    def _post(self, request):
        return self._session.post(request.uri,
                                  data=request.params,
                                  timeout=self._timeout)
