#!/usr/bin/env python3
"""tags: functions for filtering and processing tags"""

from . import log as _log

log = _log.getChild('tags')

def tagstring_to_tags(tagstring):
    """
    >>> tagstring_to_tags('a,b, c')
    ['a', 'b', 'c']
    >>> tagstring_to_tags('a,-b, -c')
    ['a', '-b', '-c']
    >>> tagstring_to_tags(',-a,b,-c') # specificially to support negation case
    ['-a', 'b', '-c']
    """
    tags = []
    tags = tagstring.split(",")
    tags = [x.strip() for x in tags]
    tags = [x for x in tags if x]
    
    return tags

def match_tags(selectors, tags):
    """ 
    Test and confirm all tags in tag_a are in tag_b, an negation is provided
    by prefixing a tag with '-' to 'carve out' a tagspace from a larger matching
    tag
    
    >>> test_tags = ['a', 'b', 'c']
    >>> match_tags(['a'], test_tags)
    True
    >>> match_tags(['a', 'b'], test_tags)
    True
    >>> match_tags(['-a', 'b'], test_tags)
    False
    >>> match_tags(['a', '-b'], test_tags)
    True
    >>> match_tags(['-a'], test_tags)
    False
    >>> match_tags(['-x'], test_tags)
    True
    >>> match_tags([], test_tags)
    True
    >>> match_tags(test_tags, [])
    False
    """
    # no possible tags to select on
    if len(tags) == 0:
        return False
        
    for test in selectors:
        if test.startswith('-'):
            if test[1:] in tags:
                return False
        else:
            if test in tags:
                return True

    return True

if __name__ == "__main__":
    import doctest
    import fission.tags
    doctest.testmod(fission.tags, verbose=True)
