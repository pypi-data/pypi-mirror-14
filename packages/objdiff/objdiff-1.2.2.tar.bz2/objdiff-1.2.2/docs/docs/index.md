# ObjDiff

ObjDiff is a library designed to give you a list of deltas between 2 trees of 
objects. This list can include item additions, deletions and modifications.

    >>> import objdiff
    >>> list(objdiff.obj_diff({'a':[1,2,3]}, {}))
    [deleted(path=['a'], val=[1, 2, 3])]
    >>>

This library may be of use to you if you deal with yaml files or have a before 
and after copy of the data and need to respond or act on specific changes 
between those 2 versions (eg spinning up more processes when the workers var is 
updated).

The src repository (obtained from [here](http://blitz.works/objdiff)) for this 
module containers 2 such yaml files to play with that model a prototype 
containers framework that can be used in conjunction with `python -m objdiff 
FILE1 FILE2` to provide a list of changes.
