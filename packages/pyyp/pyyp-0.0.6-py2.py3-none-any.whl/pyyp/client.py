# -*- coding: utf-8 -*-

"""
pyyp.client
~~~~~~~~~~~

This module provides the http client for Yunpian.
"""

import logging

import requests

from .exceptions import RequestException, Timeout
from .utils import encode_params

logger = logging.getLogger(__name__)


class Client(object):
    """Client to send requests"""

    def __init__(self, timeout):
        self._session = requests.session()
        self._timeout = timeout

    def get(self, request):
        return self._request(
                'get',
                request.url,
                params=request.params,
                timeout=self._timeout)

    def _request(self, method, url, **kwargs):
        params = encode_params(kwargs.get('params'))
        data = encode_params(kwargs.get('data'))
        logger.info('sending request. url=%s method=%s params=%r data=%r '
                    'timeout=%s', url, method, params, data, kwargs['timeout'])
        try:
            r = self._session.request(method, url, **kwargs)
            logger.info('received response. url=%s method=%s status_code=%s '
                        'text=%s', url, method, r.status_code, r.text)
            return r
        except requests.exceptions.Timeout as e:
            logger.error('request timeout. %s', e)
            raise Timeout(e)
        except requests.exceptions.RequestException as e:
            logger.error('request error. %s', e)
            raise RequestException(e)

    def post(self, request):
        return self._request(
                'post',
                request.url,
                data=request.params,
                timeout=self._timeout)
