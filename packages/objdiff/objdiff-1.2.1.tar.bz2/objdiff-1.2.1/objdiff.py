#!/usr/bin/env python3.4
"""ObjDiff: Generate a list of commands/delta to go from oe object to another

Objdiff provides 4 types of action that can be applied to an object to transtion
it to another object. one of these is internal and can be ignored

 * deleted
 * added
 * modified
 * equal (internal)

These are all namedtuples and provide the paths and values required for the 
transition

Diffing lists and dictonaries is handled diffrently and broken out into 2 functions
named diff_list and diff_dict. These provide 'shallow' diffing of objects. In the
case of dictonaries this is limited to only keys, while lists will diff the values
in a shallow fashion

The main (deep) diffing function is 'obj_diff', this takes 2 objects and provides
a stream of commands to apply via iteration

A utility is provided if this module is executed as a comamnd to show off the 
delta functionality and will diff 2 yaml files provided on the command line. The
src repository for this module provides such example yaml files
"""

__version__ = '1.2.1'
__author__ = "Da_Blitz"
__email__ = "code@pocketnix.org"
__license__ = "BSD 2 Clause"
__url__ = "http://blitz.works/objdiff"

from collections.abc import Mapping
from collections import namedtuple
import difflib

deleted = namedtuple('deleted', 'path val')
added = namedtuple('added', 'path val')
modified = namedtuple('modified', 'path old new')
equal = namedtuple('equal', 'path old new')


def obj_diff(obj1, obj2, path=[]):
    """Takes 2 objects and provides a list of comamnds to transition between the two
    
    obj1: the object to transition from
    obj2: the object to transition to
    path: Internal object used during recursion
    
    returns: generator yeilding namedtuples of operations
    """
    if type(obj1) != type(obj2):
        yield modified(path, obj1, obj2)
    # we know both obj1 and 2 have the same type
    # here as implied by the first if clause
    elif isinstance(obj1, Mapping):
        differ = {list: diff_list,
                  tuple: diff_list,
                 }.get(obj1.__class__, diff_dict)
            
        for action in differ(obj1, obj2):
            new_path = path.copy()
            new_path += action.path

            if isinstance(action, (added, deleted, modified)):
                cls = action.__class__
                yield cls(new_path, *action[1:])
            elif isinstance(action, equal):
                # no change at this node, perhaps the children have changed?
                yield from obj_diff(action.old, action.new, path=new_path)

    # this code here is for scalers/values
    elif obj1 == obj2:
        yield equal(path, obj1, obj2)
    else:
        yield modified(path, obj1, obj2)


def diff_list(a, b):
    """Get a list of commands to transition a list from one to the other
    
    a: the object to transition from
    b: the object to transition to
    
    returns: generator yeilding namedtuples of operations
    """    
    # replace, delete, insert, equal
    diff = difflib.SequenceMatcher(a=a, b=b)
    
    for action, a_start, a_end, b_start, b_end in diff.get_opcodes():
        a_last, b_last = a_end - 1, b_end - 1
        if action == 'insert':
            for i in range(b_start, b_end):
                yield added([i], b[i])
        elif action == 'delete':
            for i in range(a_start, a_end):
                yield deleted([i], a[i])
        elif action == 'equal':
            for i in range(b_start, b_end):
                yield equal([i], a[i], b[i])
        elif action == 'replace':
            if (a_end - a_start) == (b_end - b_start):
                for i1, i2 in zip(range(a_start, a_end), range(b_start, b_end)):
                    yield modified([b_last], a[i1], b[i2])
            else:
                # explicit -1 here to skip the last element
                # ie not sementically equivalent with a_last
                for i in range(a_start, a_end - 1):
                    yield deleted([i], a[i])
                yield modified([b_end-1], a[a_last], b[b_last])


def diff_dict(a, b):
    """Get a list of commands to transition a list from one to the other

    a: the object to transition from
    b: the object to transition to
    
    returns: generator yeilding namedtuples of operations
    """
    # set methods are nice and handy, hence the conversion
    a_keys = frozenset(a.keys())
    b_keys = frozenset(b.keys())

    added_keys = b_keys.difference(a_keys)
    deleted_keys = a_keys.difference(b_keys)    
    same_keys = a_keys & b_keys
    
    for key in same_keys:
        yield equal([key], a[key], b[key])
    
    for key in deleted_keys:
        yield deleted([key], a[key])

    for key in added_keys:
        yield added([key], b[key])


def deep_update(base, updates):
    """A 'deep'/recursive version of the 'update' method on dictonaries
    works on lists and other containers as well
    
    The example below is taken from the READEME as one of the tricks/patterns that occurs commonly
    >>> base = {'a': {1:1, 2:2, 3:3}, 'b': None}
    >>> updates = {'a': {1:None}}
    >>> deep_update(base, updates)
    >>> base
    {'a': {1: None, 2: 2, 3: 3}, 'b': None}
    """
    commands = obj_diff(base, updates)
    for cmd in commands:
        if isinstance(cmd, modified):
            ptr = base
            # we need the last key for making the update
            for key in cmd.path[:-1]:
                ptr = ptr[key]
            ptr[cmd.path[-1]] = cmd.new


def main():
    from argparse import ArgumentParser, FileType
    from yaml import safe_load as load
    import blessings
    import sys

    args = ArgumentParser()
    args.add_argument('old', metavar="OLD_FILE", type=FileType('r'),
                    help="The original state to diff against")
    args.add_argument('new', metavar="NEW_FILE", type=FileType('r'),
                    help="The new state that we want to be in")
    
    options = args.parse_args()
    
    old = load(options.old)
    new = load(options.new)

    t = blessings.Terminal()

    for cmd in obj_diff(old, new):
        path = '.'.join(cmd.path)
        if isinstance(cmd, modified):
            print("{t.yellow_bold}!{t.normal} {path}: {cmd.old} {t.bold}=>{t.normal} {cmd.new}".format(**locals()))
        elif isinstance(cmd, deleted):
            print("{t.red_bold}-{t.normal} {path}: {cmd.val}".format(**locals()))
        elif isinstance(cmd, added):
            print("{t.green}+{t.normal} {path} {cmd.val}".format(**locals()))

if __name__ == "__main__":
    main()
