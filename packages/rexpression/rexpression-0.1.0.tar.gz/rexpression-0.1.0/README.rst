python-rexpression
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/rexpression.svg?branch=master
    :target: http://travis-ci.org/lambdalisue/rexpression
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/rexpression/badge.svg?branch=master
    :target: https://coveralls.io/r/lambdalisue/rexpression/
    :alt: Coverage

.. image:: https://img.shields.io/pypi/dm/rexpression.svg
    :target: https://pypi.python.org/pypi/rexpression/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/rexpression.svg
    :target: https://pypi.python.org/pypi/rexpression/
    :alt: Latest version

.. image:: https://img.shields.io/pypi/format/rexpression.svg
    :target: https://pypi.python.org/pypi/rexpression/
    :alt: Format

.. image:: https://img.shields.io/pypi/status/rexpression.svg
    :target: https://pypi.python.org/pypi/rexpression/
    :alt: Status

.. image:: https://img.shields.io/pypi/l/rexpression.svg
    :target: https://pypi.python.org/pypi/rexpression/
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/rexpression.svg
    :target: https://pypi.python.org/pypi/rexpression/
    :alt: Support version

Add Perl like regular expression syntax like:

.. code:: python

    from rexpression import regex

    print("foo bar" ==~ regex("^foo"))   # -> True
    print("foo bar" ==~ regex("^boo"))   # -> False

    print("foo bar" !=~ regex("^foo"))   # -> False
    print("foo bar" !=~ regex("^boo"))   # -> True

    print("foo bar" == regex("foo"))     # -> False
    print("foo bar" == regex("boo"))     # -> False
    print("foo bar" == regex("foo bar")) # -> True

**DO NOT USE THIS MODULE EXCEPT FOR A PIECE OF CODE**.
Basically, this is really **BAD** idea in Python and you should prevent to use this kind of BAD syntax in productive code.


Installation
------------
Use pip_ like::

    $ pip install python-rexpression

.. _pip:  https://pypi.python.org/pypi/pip


License
-------------------------------------------------------------------------------
The MIT License (MIT)

Copyright (c) 2015 Alisue, hashnote.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
