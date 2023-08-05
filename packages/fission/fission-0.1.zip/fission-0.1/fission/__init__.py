#!/usr/bin/env python

__version__ = "0.1"
__email__ = "code@pocketnix.org"
__author__ = "Da_Blitz"
__license__ = "BSD (3 Clause)"
__url__ = "http://blitz.works/fission"

import logging as _logging

log = _logging.getLogger('fission')
formatter = _logging.Formatter("%(name)-15s %(levelname)-8s %(asctime)10s %(process)s: %(message)s")

