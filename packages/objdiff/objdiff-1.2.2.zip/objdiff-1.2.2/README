Objdiff
=======
Take 2 sets of containers and provide a (deep) delta between them

This module is used by the author to diff yaml files and on disk file trees
and best work out how to transition from one state to another (mainly for 
work with containers).

**Note:** Requires Python 3.3 or greater due to use of '`yield from`'

How?
----
Objdiff uses `difflib` built into python for lists and tuples (basically sorted 
things) and implements its own comparison code for dictionaries. User types are 
detected via the `collections.abc.Mapping <https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes>`_ 
type and instance comparison and are treated as dictionaries (ie unsorted item 
=> value mappings)

What does this look like?
-------------------------
    >>> import objdiff
    >>> a = {'a': 1, 'b':[1,2,3], 'c':None}
    >>> b = {'a': 1, 'b':[1,4], 'c':'hello'}
    >>> objdiff.obj_diff(a, b)
    <generator object obj_diff at 0xb6a3da80>

We return an iterator and make use of yield from so you can process large trees 
of objects efficiently and incremental

    >>> from pprint import pprint
    >>> pprint(list(objdiff.obj_diff(a, b)))
    [modified(path=['c'], old=None, new='hello'),
     modified(path=['b'], old=[1, 2, 3], new=[1, 4]),
     equal(path=['a'], old=1, new=1)]
    
Expanding out the generator we get back a bunch of tuples containing the 
command value, key path, before and after value

    >>> c = {'a':{1: None, 2: 2, 3: 3}, 'b': None}
    >>> d = {'a':{1: 1, 2: 2}, 'b': {'1':{}, '2':{'2':2}}}
    >>> pprint(list(objdiff.obj_diff(c, d)))
    [modified(path=['b'], old=None, new={'1': {}, '2': {'2': 2}}),
     modified(path=['a', 1], old=None, new=1),
     equal(path=['a', 2], old=2, new=2),
     deleted(path=['a', 3], val=3)]
    
**Note:** in the above how you get a full list of keys to the destined object after 
the command value.

In total there are 4 types of command, as listed below with one internal type
that can be ignored.

 * added
 * deleted
 * modified
 * equal (internal, scalar values are equal)

More documentation can be found at `Blitz works docs <http://docs.blitz.works/objdiff>`_
