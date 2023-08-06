#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    08.04.2016 11:43:47 CEST
# File:    _export.py

import importlib

__all__ = ['test_doc', 'export']

enable_doc_test = False

def test_doc(enable=True):
    """Test whether exported objects have a non-zero docstring. This must be called before the module is imported.

    :param enable:  Determines whether the test should be enabled or disabled.
    """
    global enable_doc_test
    enable_doc_test = enable

def export(obj):
    """Adds the decorated object to its module's ``__all__``."""
    mod = importlib.import_module(obj.__module__)
    # add to __all__
    try:
        mod.__all__.append(obj.__name__)
    except AttributeError:
        mod.__all__ = [obj.__name__]

    # test if the docstring is nonzero
    if enable_doc_test:
        if not obj.__doc__:
            raise AssertionError("'{}' does not have a non-zero docstring.".format(obj.__name__))

    return obj
