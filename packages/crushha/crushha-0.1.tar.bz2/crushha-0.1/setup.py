#!/usr/bin/env python

name = 'crushha'
path = 'crushha'


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
    packages = [path], # corresponds to a dir 'epicworld' with a __init__.py in it
    author = "Da_Blitz",
    author_email = "code@pocketnix.org",
    maintainer=None,
    maintainer_email=None,
    description = "Define HA domains with CRUSH maps",
    long_description = readme,
    license = "ISC",
    keywords = "crush CRUSH ha ceph containers",
    download_url = "http://blitz.works/crushha/archive/tip.zip",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing",
    ],
    platforms=None,
    url = "http://blitz.works/crushha",
    zip_safe = True,
    
    # needed if you are using distutils extensions for the build process
    setup_requires = ['hgdistver'],

    # optinal packages needed to install/run this app
    install_requires = ['distribute'],

    # extra packages needed for the test suite
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
