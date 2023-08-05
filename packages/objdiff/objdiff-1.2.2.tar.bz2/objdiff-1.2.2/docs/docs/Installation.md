# Installation

ObjDiff makes use of the `yield from` statement in Python 3.3 or greater and as 
such the minimum supported version of Python is 3.3.

ObjDiff is a fully self contained pure python module with no dependencies 
beyond the stdlib. As such a simple pip install will install the package.

    $ pip install objdiff

Note that it is not recommended to do this as root. if you need this available to 
all code running under your current user please install the module user wide 
with the following command:

    $ pip install --user objdiff

If the module needs to be accessible to a different user please consider using a 
virtualenv or installing a package provided by the OS that contains the objdiff 
library.


## Developers

If you are hacking on the source for objdiff, several commands in the Makefile 
have been provided to get a standard environment up quickly.

to build a virtual environment to a standard location use the following command:

    $ make virtual

This will proceed to build a virtual environment that you can then activate for 
your current shell with the following command:

    $ . venv/bin/activate

Your current python installation is now separate from the Operating System 
provided one allowing you to add packages without root privileges.

To activate the ObjDiff source repository as a module in your new virtual 
environment, issue the following command.

    $ make develop

This will activate the module in such a way that any changes made to the module 
itself are reflected instantly without having to re-install the module every 
time.
