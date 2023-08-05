Python pymongo modem
===============================

.. image:: https://travis-ci.org/internap/python-pymongomodem.svg?branch=master
:target: https://travis-ci.org/internap/python-pymongomodem

.. image:: https://img.shields.io/pypi/v/python-pymongomodem.svg?style=flat
:target: https://pypi.python.org/pypi/python-pymongomodem

.. image:: https://img.shields.io/github/release/internap/python-pymongomodem.svg?style=flat
:target: https://github.com/internap/python-pymongomodem/

Usage
-----
.. code:: python

    from pymongomodem.utils import encode_input, decode_output

    @decode_output
    def _get_entities_from_db(self, args):
        return list(self.db.entity.find(args, {"_id": 0}))

    @decode_output
    def _get_one_entity_from_db(self, args):
        return self.db.entity.find_one(args, {"_id": 0})

Why
-----
While using pymongo we ran into the issue of storing key using dot (.)

This small piece of python simply convert it so that we alway play with python dict.

for in-depth example of what it does see https://github.com/internap/python-pymongomodem/blob/master/tests/pymongomodem_test.py
