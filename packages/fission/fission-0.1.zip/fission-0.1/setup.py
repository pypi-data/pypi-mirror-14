#!/usr/bin/env python

name = 'fission'
path = 'fission'

from setuptools import setup, find_packages

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
    # use one of the following 3 optons
    packages = [path], # corresponds to a dir 'epicworld' with a __init__.py in it
    author = "Da_Blitz",
    author_email = "code@pocketnix.org",
    maintainer=None,
    maintainer_email=None,
    description = "Container managment software",
    long_description = readme,
    license = "MIT BSD",
    keywords = "container",
    download_url="http://blitz.works/fission",
    classifiers=None,
    platforms=None,
    url = "http://blitz.works",

    entry_points = {"console_scripts":["fission = fission.cli:main",
                                      ],
                   },
#    scripts = ['scripts/dosomthing'],
    zip_safe = True,
    setup_requires = ['hgdistver'],
    install_requires = ['yaml', 'jinja2'],
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
