# Examples

Usage of the ObjDiff library is mainly centered around one primary function, 
`objdiff.obj_diff`. This function provides the difference between 2 object 
hierarchies as a list of commands with full key path and value changes as shown 
in the example below:

    >>> import objdiff
    >>> a = {'a': 1, 'b':[1,2,3], 'c':None}
    >>> b = {'a': 1, 'b':[1,4], 'c':'hello'}
    >>> objdiff.obj_diff(a, b) # doctest: +ELLIPSIS
    <generator object obj_diff at ...

By default `objdiff` returns an iterator of commands rather than a list as it 
was primarily intended to work with large, lazily loaded data structures. 
Expanding it out by forcing it via `list()` provides a sequence of commands as 
shown below:

    >>> from pprint import pprint
    >>> pprint(sorted(objdiff.obj_diff(a, b)))
    [equal(path=['a'], old=1, new=1),
     modified(path=['b'], old=[1, 2, 3], new=[1, 4]),
     modified(path=['c'], old=None, new='hello')]
    
In total there are 4 types of command with one being internal, but exposed as 
it may be useful to your application. ie:

 * added
 * deleted
 * modified
 * equal (internal, indicates 2 scalar values are equal)

These commands represent changes in a 'deep' fashion and will contain the 
minimal set of changes (in terms of scope of change, or the minimal amount of 
data to change) to go from one object tree to another. The example below shows 
changes to a non root value along with some of the other primitive operations:

    >>> c = {'a':{1: None, 2: 2, 3: 3}, 'b': None}
    >>> d = {'a':{1: 1, 2: 2}, 'b': {'1':{}, '2':{'2':2}}}
    >>> pprint(sorted(objdiff.obj_diff(c, d))) #doctest: +SKIP
    [modified(path=['a', 1], old=None, new=1),
     equal(path=['a', 2], old=2, new=2),
     deleted(path=['a', 3], val=3),
     modified(path=['b'], old=None, new={'1': {}, '2': {'2': 2}})]
