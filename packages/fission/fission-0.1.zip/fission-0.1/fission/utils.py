#!/usr/bin/env python3
"""Main cli entry points"""

from argparse import ArgumentTypeError
from . import formatter, log as _log

log = _log.getChild("utils")

def convert_bool(s):
    """Convert the inut as best we can to a boolean value or fail
    
    Possible inputs
    ================
    Yes, yes
    No, no
    True, TRUE, true
    False, FALSE, false
    1, 0
    
    Raises
    =======
    ValueError: No known value matched the input
    """
    s = s.lower()
    
    val = None
    
    if s in ('1', 'yes', 'true'):
        val = True
    elif s in ('0', 'no', 'false'):
        val = False    
    else:
        raise ArgumentTypeError("Input matched no known boolean value: " + s)
    
    return val
    
