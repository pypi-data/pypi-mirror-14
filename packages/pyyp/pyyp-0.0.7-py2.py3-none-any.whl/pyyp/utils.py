# -*- coding: utf-8 -*-

"""
pyyp.utils
~~~~~~~~~~~

This module provides utils.
"""


def encode_params(data):
    if data is None:
        return data

    kvs = []
    for k, v in data.items():
        if k == 'apikey':
            v = mask_api_key(v)

        kvs.append((k, v))

    kvs.sort()

    pairs = []
    for p in kvs:
        pairs.append('='.join(p))

    return '&'.join(pairs)


def mask_api_key(v):
    text_len = 4
    parts = [v[:text_len], '****', v[-text_len:]]
    return ''.join(parts)
