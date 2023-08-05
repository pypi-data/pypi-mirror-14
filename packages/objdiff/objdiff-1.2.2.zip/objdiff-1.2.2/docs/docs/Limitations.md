# Limitations

Objdiff has a couple of known limitations that may not be immediately obvious.

## Root objects must be dictionaries

ObjDiff currently assumes that the root object is a dictionary, using scalars or lists
is not guaranteed to work.

This may change in the future with the list case being the hardest code for.

## ObjDiff makes use of yield from

ObjDiff makes use of the `yield from` statement introduced in python 3.3 to 
simplify part of its code base. While this limitation could be removed there is 
extra complexity that comes with it and all known uses of this module for the 
author have so far been on python 3.4 or greater.

This is unlikely to change without a good reason, large project needing the 
module or changing requirements of the author.

At this time '_Supporting python 2.7_' or '_lots of people use python 2_' is not 
considered a good reason to provide such functionality.
