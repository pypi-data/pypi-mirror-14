Introduction
============

This module implements new, configurable data types that are intended to be
used along with Py3o templates.

These data types should be used in the data source dictionary, as a
replacement to builtin (int, float...) and standard (date, time...) types.
Their rendering is based on a configuration that can be saved and loaded
as custom properties inside a ODF file.

Full Documentation
==================

We `provide a documentation`_ for this package.

Changelog
=========

0.1 Apr. 14 2016
----------------

  - Py3o types for integer, float, date, time, datetime
  - Import/export configuration from the custom settings of a ODF file
  - JSON encoding and decoding

.. _provide a documentation: http://py3o-types.readthedocs.org
