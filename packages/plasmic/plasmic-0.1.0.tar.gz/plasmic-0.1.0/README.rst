Plasmic
=======

Configuration files with a Python-like syntax
---------------------------------------------

Parse a very Python-like mini-language to produce a dictionary.  This
allows Python programs to be configured using a Python-like language
consisting of dictionaries, tuples, and literal values.  Plasmic
dictionary keys must be literal values.  Plasmic dictionary values can
be literal values and, possibly nested, tuples and other plasmic
dictionaries.

The plasmic Python-like language contains almost no expression
evaluation.  The single, optional, expression allowed is a
``string.Formmatter.format()`` formatting syntax used for
interpolation -- the insertion of of data into values by reference to
Plasmic dictionary keys.

As a convenience all dictionary entries keyed by symbols have their
keys converted to the lower case string equivalent.  The following 2
examples are equivalent:

A configuration with symbols for keys::

  {section1:
    {key1: "value1",
     key2: 2},
   Section2:
    {Key1: "othervalue",
     KEY3: 3.0}
  }

The identical configuration with strings for keys::

  {"section1":
    {"key1": "value1",
     "key2": 2},
   "section2":
    {"key1": "othervalue",
     "key3": 3.0}
  }

Although the symbols are written in mixed case the end result is a
dictionary keyed with strings in lower case.

The recommended suffix for files written in the Plasmic language is:
``.pcf``

Plasmic has the following sub-projects to support configuring
applications using files written in Plasmic.  Most users will not want
to use plasmic directly but will import one of these sub-projects.


plasmic.configparser
--------------------

A ``configparser``-like API for the reading and writing of
configuration files in plasmic syntax.

::

   import plasmic.configparser


plasmic.montague
----------------

A plugin allowing Plasmic configuration files to drive the
``Montague`` WSGI component loader.
