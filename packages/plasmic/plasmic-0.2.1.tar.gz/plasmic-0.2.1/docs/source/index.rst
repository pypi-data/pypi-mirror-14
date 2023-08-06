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



The Plasmic Configuration System
================================

Plasmic parses a very Python-like mini-language to produce a
dictionary.  This allows Python programs to be configured using a
Python-like language.

Here is a sample configuration::

  {section1:
    {key1: "value1",
     key2: 2},
   section2:
    {key1: "othervalue",
     key3: 3.0
     subsection1:
      {key4: (1, 2, 3)
       key5: {"foo": "meta",
              "bar": "syntactic"}
      }
    }
  }

.. index::
   single: syntax
   single: dictionaries
   single: tuples
   single: literals

The Plasmic language consists of dictionaries, tuples, and literal
values.  Plasmic dictionary keys must be literal values.  Plasmic
dictionary values can be literal values and, nested when desired,
tuples and plasmic dictionaries.

.. index::
   single: interpolation

Plasmic allows values to be designated once and used in multiple
places within a configuration.  This is commonly called interpolation.
Plasmic replaces reference to configuration keys with the key's value.

.. index::
  single: suffix
  pair: recommended; suffix
  single: .pcf

The recommended suffix for files written in the Plasmic language is:
``.pcf``


.. index:: pair: narrative; documentation

Narrative Documentation
-----------------------

.. toctree::
   :maxdepth: 2

   why
   syntax


.. index::
  single: support

Support
-------

.. index:: single: mailing list

.. index::
  single: mailing list; archives
  single: mailing list; signup

.. index:: single: bug tracker

* Mailing List (plasmic atsign googlegroups period com) -- non-members
  may post
* `Mailing List Signup and Archives
  <https://groups.google.com/forum/#!forum/plasmic>`_
* `Bug Tracker
  <https://bitbucket.org/karlpinc/plasmic/issues?status=new&status=open>`_


.. index::
  pair: development; resources

Development
-----------

.. index:: single: source code

.. index::
  single: resources for contributors
  pair: contributor; resources

* `Source Code <https://bitbucket.org/karlpinc/plasmic/src>`_
* `Resources for Contributors <https://bitbucket.org/karlpinc/plasmic>`_


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

