#!/usr/bin/env python3
"""A library to verify that arbitrary object graphs have a certin shape

can be used to manipulate object graphs to match the desired state, eg
adding in values that are missing or casting scalars to specific types

syntax:
 collections (dictonaries and lists, or iterable objects in general)
  can have a specific key chosen with [key]. by seperating the keys
  with commas, multiple values can be returned. setting key to "*" 
  causes the rule to match on all instances in that collection. if 
  "*" is the first argument followed by a comma seprated list of values
  with '-' in them then all values except the ones specified are returned
  "**" is used to specify the leaves of an object tree from that point
  (ie the deepest values in the tree, no intermediates)
  eg:
    "mynames[dablitz]": returns a single object
    "mynames[dablitz,da_blitz]": returns matches for dablitz and da_blitz
    "mynames[*]: returns all all objects in mynames
    "mynames[*,-dablitz]: returns all all objects except ones dablitz
    
More complex examples:
    "config[defaults][hostname]"
"""

from . import log as _log
import yaml

log = _log.getChild('verify')


#a = list(yaml.scan("blah: 3"))
#In [61]: s = list(yaml.parse("blah: 3\nha:\n - 1\n - 2\n - 3"))
#
#In [62]: s
#Out[62]:
#[StreamStartEvent(),
# DocumentStartEvent(),
# MappingStartEvent(anchor=None, tag=None, implicit=True),
# ScalarEvent(anchor=None, tag=None, implicit=(True, False), value='blah'),
# ScalarEvent(anchor=None, tag=None, implicit=(True, False), value='3'),
# ScalarEvent(anchor=None, tag=None, implicit=(True, False), value='ha'),
# SequenceStartEvent(anchor=None, tag=None, implicit=True),
# ScalarEvent(anchor=None, tag=None, implicit=(True, False), value='1'),
# ScalarEvent(anchor=None, tag=None, implicit=(True, False), value='2'),
# ScalarEvent(anchor=None, tag=None, implicit=(True, False), value='3'),
# SequenceEndEvent(),
# MappingEndEvent(),
# DocumentEndEvent(),
# StreamEndEvent()]
#
#s = a[0]
#
#In [33]: s.start_mark.get_snippet()
#Out[33]: '    blah: 3\n    ^'
   

def is_type(*types):
    @wraps(is_type)
    def inner(val):
        return isinstance(val, types)
    
    return inner


class ObjVerifier:
    def __init__(self, root, key, _parent=None, path=None):
        self._root = root
        self._keys = key.split(',')
        if not self._keys:
            raise ValueError("key does not match anything")
        self._parent = _parent
        self._path = path if path else []
    
    def __eq__(self, val):
        keys = self._keys

        if keys[0] == '*':
            # all with subtractive
            ignore = keys[1:]
            keys = get_orig_keys()
            keys -= ignore
        else:
            # do all keys
            for key in keys:
                pass
        
#        >>> d['a']['b']['c'] = 3
#        >>> functools.reduce(operator.getitem, ('a', 'b', 'c'), d)
#        >>> 3
        from functools import reduce
        from operator import getitem
        for path in self.path + (self._keys,):
            value = reduce(getitem, path, self._root)
            value == val

    def __getitem__(self, key):
        return self.__class__(self._root, key, _parent=self, path=self.path + [(self._keys,)])


#try:
#    config = obj
#    # this
#    if config['blah']['blah'].value == None:
#        config['blah']['blah'].value = []
#    # is the same as
#    config['blah']['blah'].replace(None, []) # upconvert values
#    config['blah']['blah'].replace(is_type(int), converter=lambda x: [x]) # invoke a function to conver value
#    #
#    config['blah']['blah'] == is_type(list)
#    config['blah']['blah'] == partial(len, 3)
#    config["*"]['name']
#    config["*"].optional('description') == is_type(str)
#    config['*,-defaults']['mykey'] == 3
#
#except SyntaxError as err:
#    pass
