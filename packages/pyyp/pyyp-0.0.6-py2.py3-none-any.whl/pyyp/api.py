# -*- coding: utf-8 -*-

"""
pyyp.api
~~~~~~~~

This module provides the basic API interface for Yunpian.
"""

from .client import Client
from .models import (
        SMSSendRequest,
        SMSSendResponse,
        SMSBatchSendRequest,
        SMSBatchSendResponse)


class Yunpian(object):
    """The core Yunpian class."""

    def __init__(self, api_key, timeout=10):
        self._api_key = api_key
        self._client = Client(timeout)

    def send(self, mobile, text):
        req = SMSSendRequest(apikey=self._api_key, mobile=mobile, text=text)
        r = self._client.post(req)
        return SMSSendResponse.parse(r)

    def send_all(self, mobiles, text):
        mobile = ','.join(mobiles)
        req = SMSBatchSendRequest(apikey=self._api_key,
                                  mobile=mobile,
                                  text=text)
        r = self._client.post(req)
        return SMSBatchSendResponse.parse(r)
