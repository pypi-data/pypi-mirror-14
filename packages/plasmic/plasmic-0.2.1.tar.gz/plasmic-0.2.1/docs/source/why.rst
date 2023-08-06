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


Why Yet Another Config Syntax?
------------------------------

The short answer is "Because there's nothing like Python's syntax for
expressing Python data."  Some syntaxes don't attempt to map to Python
data types, your program must manually handle type conversion.  Other
syntaxes are serializations of data expressed in other languages.
These are more expressive, both in data type and data structure
complexity, but because they are syntaxes designed to express data it
remains for an interpolation mechanism to be tacked on.  Python
syntax is the ideal choice for Python data representation and
manipulation.

Plus, Python exposes it's own internals making it easy to write
powerful Python-like parsers that are, at the same time, safe.
Plasmic configuration files may look like Python but they cannot be
abused to execute arbitrary code or, for that matter, any sort of
code at all.
