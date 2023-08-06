pyyp
====

.. image:: https://travis-ci.org/pragkent/pyyp.svg?branch=master
    :target: https://travis-ci.org/pragkent/pyyp

.. image:: https://codecov.io/github/pragkent/pyyp/coverage.svg?branch=master
    :target: https://codecov.io/github/pragkent/pyyp?branch=master

pyyp is a wrapper of the *Yunpian SMS* API, written in Python.

Installation
------------

To install pyyp, simply:
.. code-block:: bash

    $ pip install pyyp


Example
-------
.. code-block:: python

    >>> yunpian = pyyp.Yunpian(api_key=API_KEY)
    >>> yunpian.send('13812345678', 'hello yunpian!')


TODO
----
- Add unit tests


