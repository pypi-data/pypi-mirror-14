#Tips and Tricks

## Path Navigation

Path navigation is one that comes up a lot when given a list of keys, To 
quickly and efficiently get a value given a list of keys making up a path try 
using the following pattern.

    >>> from functools import reduce
    >>> from operator import getitem
    >>> path = ['a', 1]
    >>> d = {'a':{1: 1, 2: 2}, 'b': {'1':{}, '2':{'2':2}}}
    >>> reduce(getitem, path, d)
    1

## Deep Updates

**Note:** As of objdiff 1.2, a function that is simmilar to the one described 
below is avalible as `objdiff.deep_update`

If you have a deep data structure made up of dictonaries (eg a config file) and 
wish to apply an 'overlay' of values from a diffrent source (eg an included 
file or a profile) then the naive way with `dict.update()` may not work well 
for you eg:

    >>> base = {'a': {1:1, 2:2, 3:3}, 'b': None}
    >>> updates = {'a': {1:None}}
    >>> base.update(updates)
    >>> base == {'a': {1: None}, 'b': None}
    True

In the above we only wanted to update obj['a'][1] to be None, however the other
keys where also overwritten.

ObjDiff will give you the full path of keys that need updating and the values 
through the 'added' command that is returned via `objdiff.obj_diff()`. These 
can then be used to deeply recurse into the data and update the correct key 
directly with the new value.

This can be demonstrated as below:

    >>> from pprint import pprint
    >>> import objdiff
    >>> base = {'a': {1:1, 2:2, 3:3}, 'b': None}
    >>> updates = {'a': {1:None}}
    >>> for cmd in objdiff.obj_diff(base, updates):
    ...     if isinstance(cmd, (objdiff.added, objdiff.modified)):
    ...         ptr = base
    ...         # we need the last key for making the update
    ...         for key in cmd.path[:-1]:
    ...             ptr = ptr[key]
    ...         ptr[cmd.path[-1]] = cmd.new
    ...
    >>> base == {'a': {1: None, 2: 2, 3: 3}, 'b': None}
    True
    
In the above you can see we ignore all commands except add and modify. Deleted 
is discarded as the update dictonary has no way to specify key deletion.
