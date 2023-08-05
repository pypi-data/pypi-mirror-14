# API

# obj_diff
**Function:** `obj_diff(old, new)`
## Description

`obj_diff` takes 2 trees of objects and returns the minimal set of changes 
(ie making the smallest possible changes to the data at once) that will 
transform the old object tree to the new object tree. The iterator of commands 
it provides back can then be used to manipulate the existing object or detect 
specific types of changes and act upon these.

## Args

**old:** The old state of the objects

**new:** The new state of the objects

Ideally these root objects should both be dictionaries, the use of lists or 
scalars at this time may fail.

## Returns
An iterator of command objects, cast to a list this looks similar to the list below:

    [modified(path=['a', 1], old=None, new=1),
     equal(path=['a', 2], old=2, new=2),
     deleted(path=['a', 3], val=3),
     modified(path=['b'], old=None, new={'1': {}, '2': {'2': 2}})]

The returned objects are of one of the following types:

 * added
 * deleted
 * modified
 * equal

These types are available under the module `objdiff` for use with `isinstance`. 
the use of `isinstance` is the recommended way to confirm which command is 
which in the stream as the implementation may change from `namedtuple` to 
something different in the future.

-------------------------------------------------------
# deep_update
**Function:** `deep_update(base, updates)`

### Description
`deep_update` is similar to `dict.update()` in the same way that `copy()` and 
`copy.deepcopy` from the `copy` module are related. It attempts to do a 'deep' 
rather than 'shallow' (ie recurse as deeply as possible rather than root key 
only) update of values and can be used to apply a deeply nested structure of 
dictionaries and lists on top of another set of dictionaries and lists.

First the structure is parsed to obtain a delta via `obj_diff`, followed by 
taking this output and using it to apply the new values on top of the old ones, 
preserving intermediate keys.

**Note:** This function updates in place on top of the base object

### Args

**base:** The base object that will be updated in place

**updates:** The values to apply on top of the base object

-------------------------------------------------------
# diff_list

**Function:** `diff_list(a, b)`

### Description

`diff_list` compares 2 lists and returns a list of commands to mutate the first 
list to be identical to the second list. This is a 'shallow' function and does 
not recurse into the intermediate values (see `obj_diff` if you need this 
functionality)

### Args

**a:** The list to be compared against

**b:** The new list to compare against

### Returns

An iterator of commands, identical to `obj_diff`

-------------------------------------------------------
# diff_dict
**Function:** `diff_dict(a, b)`

### Description

`diff_dict` compares 2 dicts and returns a list of commands to mutate the first 
dict to be identical to the second dict. This is a 'shallow' function and does 
not recurse into the intermediate values (see `obj_diff` if you need this 
functionality)

### Args

**a:** The dictionary to be compared against

**b:** The new dictionary to compare against

### Returns

An iterator of commands, identical to `obj_diff`

-------------------------------------------------------
# command types

**Class:** `added(path, val)`

**Class:** `deleted(path, val)`

**Class:** `modified(path, old, new)`

**Class:** `equal(path, old, new)`

### Description

These 4 classes represent the core command list to transition one object 
hierarchy to another. These commands are normally returned via iteration and 
the official way to determine which command is being provided is via the use of 
`isinstance`.

### Args

**path:** A list of keys from the root object to the leaf object.

**val:** The Value that changed (applicable to `added` and `deleted` only).

**old:** A reference to the old value to change from.

**new:** A reference to the new value to change to.

**Note:** equal provides both `old` and `new` rather than just `val` as it is 
used to pass the old object hierarchy back for further iteration. For this 
values are provided with `new` being the value that should always be chosen for 
updates (use of `old` in an update may lead to issues if mutating the old 
object tree).
