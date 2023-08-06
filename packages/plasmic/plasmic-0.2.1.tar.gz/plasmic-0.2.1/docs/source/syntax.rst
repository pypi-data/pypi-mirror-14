.. Copyright (C) 2016 The Meme Factory, Inc.  http://www.meme.com/

   This file is part of Plasmic.
  
   Plasmic is free software: you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   Plasmic is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.
  
   You should have received a copy of the GNU Lesser General Public License
   along with Plasmic.  If not, see <http://www.gnu.org/licenses/>.

   Karl O. Pinc <kop@meme.com>

.. index::
   single: syntax

More About Syntax
-----------------

The Plasmic mini-language differs from Python in 2 major ways.  First,
the only expressions allowed are those that support interpolation.
Second, when symbols are used as dictionary keys they are converted to
lower-case strings.


Symbols
^^^^^^^

.. index::
   single: symbols
   pair: free; symbols

As a convenience all dictionary entries keyed by symbols have their
keys converted to the lower case string equivalent.  The following 2
examples are equivalent:

.. note::

   The following is here only as an example.  It is bad practice in
   Plasmic to write symbols containing upper case letters.

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

.. tip::

   Keys containing periods, plus signs, parenthesis, or anything else
   that make them look like Python expressions cannot be written as
   symbols.  Write them as strings, using the usual Python string
   quoting syntax.

Symbols cannot be used as keys instead of strings in dictionarys
contained in tuples.

The following is invalid syntax::

  {"section1":
    {"key1": ("one",
              "two",
              {many: 3, lots: 4})
    }
  }


.. index:: single: interpolation

Interpolation
^^^^^^^^^^^^^

The plasmic Python-like language contains almost no expression
evaluation.  The single, optional, expression allowed is a
``string.Formmatter.format()`` formatting syntax used for
interpolation -- the insertion of of data into values by reference to
Plasmic dictionary keys.
