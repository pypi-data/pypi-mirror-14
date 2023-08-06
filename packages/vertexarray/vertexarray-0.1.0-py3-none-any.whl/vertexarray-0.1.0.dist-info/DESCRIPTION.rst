VertexArray
===========

A simple library for efficiently storing & manipulating vertex arrays in python.

Requirements
------------

1. Python 3.+

This library is pure python 3 and has no other requirements.

Installation
------------

`python3 setup.py install`

Usage
-----

```python

>>> from vertexarray import VertexArray
>>> va = VertexArray()
>>> face = va.extend([(1, 0, 0), (0, 1, 0), (0, 0, 1)])

```

0.1.0 (2016-04-06)
------------------

- Initial development version, copied & renamed from maze-builder.

