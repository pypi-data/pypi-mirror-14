#!/usr/bin/env python
from __future__ import print_function

name = 'objdiff'
path = 'objdiff'

import sys
BIG_ERROR=1
if sys.version_info < (3,3):
    print("This module requires at least python 3.3 due to use of yield from")
    sys.exit(BIG_ERROR)
    

## Automatically determine project version ##
from setuptools import setup, find_packages
try:
    from hgdistver import get_version
except ImportError:
    def get_version():
        import os
        
        d = {'__name__':name}

        # handle single file modules
        if os.path.isdir(path):
            module_path = os.path.join(path, '__init__.py')
        elif os.path.isfile(path + '.py'):
            module_path = path + '.py'
        else:
            module_path = path
                                                
        with open(module_path) as f:
            try:
                exec(f.read(), None, d)
            except:
                pass

        return d.get("__version__", 0.1)

## Use py.test for "setup.py test" command ##
from setuptools.command.test import test as TestCommand
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

## Try and extract a long description ##
for readme_name in ("README", "README.rst", "README.md"):
    try:
        readme = open(readme_name).read()
    except (OSError, IOError):
        continue
    else:
        break
else:
    readme = ""

## Finally call setup ##
setup(
    name = name,
    version = get_version(),
    author = "Da_Blitz",
    author_email = "code@pocketnix.org",
    maintainer=None,
    maintainer_email=None,
    description = "Returns a list of commands/delta to go from one tree of objects to another",
    long_description = readme,
    license = "MIT BSD",
    keywords = "objects diff tree difflib patch diffrence",
    download_url='http://blitz.works/objdiff/archive/default.zip',
    classifiers= [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=None,
    url = "http://blitz.works/objdiff",
    zip_safe = True,
    
    # needed if you are using distutils extensions for the build process
    setup_requires = ['hgdistver'],

    # optinal packages needed to install/run this app
    install_requires = ['distribute'],

    # extra packages needed for the test suite
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
