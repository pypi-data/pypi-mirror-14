``iso4217``: Currency data package for Python
=============================================

.. image:: https://badge.fury.io/py/iso4217.svg?
   :target: https://pypi.python.org/pypi/iso4217
.. image:: https://travis-ci.org/spoqa/iso4217.svg?branch=master
   :target: https://travis-ci.org/spoqa/iso4217

This Python package contains `ISO 4217`_ currency data, represented as
enum_ module which was introduced in 3.4.  Note that this works on Python 2.5
as well as 3.4, the latest version of Python, through enum34_ package.

>>> from iso4217 import Currency
>>> Currency.usd.code
'USD'
>>> Currency.usd.currency_name
'US Dollar'
>>> Currency.usd.exponent  # USD has cents
2
>>> Currency.jpy.currency_name
'Yen'
>>> Currency.jpy.exponent  # JPY has no minor units
0

Written by `Hong Minhee`_.  Distributed under Public Domain.


.. _ISO 4217: http://www.iso.org/iso/home/standards/currency_codes.htm
.. _enum: https://docs.python.org/3/library/enum.html
.. _enum34: https://pypi.python.org/pypi/enum34
.. _Hong Minhee: http://hongminhee.org/
