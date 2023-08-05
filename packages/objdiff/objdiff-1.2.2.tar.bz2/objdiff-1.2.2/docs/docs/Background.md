# Background

Original use case
------------------
This module is the offshoot of a proof of concept project. This project would 
allow you to manage containers in a GUI environment in a browser and would spit 
out 2 yaml files, One with the the node/server information and another with the 
positioning information. When a user clicked submit this would be checked into 
version control. When a user decided to push to production the current state of 
the system would be diff'd using this library against the desired state and the 
command list generated would be used to work out how to manipulate the 
environment to match the new setup.

Why not another lib?
---------------------
At the time of this library's inception, no other module that provided easy 
access to the key path was available. While several options exist it is not 
immediately obvious how to get at this information when playing around with them 
for a brief amount of time.

How?
----
The difflib in python operates on lists of strings internally and can 
be adapted to work on generic lists of items. This forms the basis of diffing 
lists. Dictionaries are handled with short custom code that looks at the keys to 
determine what has been added, deleted and modified. User types are detected 
via the collections.abc.Mapping [Abstract base class](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes) 
and are treated as dictionaries (ie unsorted item => value mappings).
