"""
This module includes utility functions that are used in other modules.
"""

import re


WORD_RE = re.compile('([A-Z]+[a-z0-9]*)')


def decamelize(s):
    """
    Convert CamelCase string to lowercase. Boundary between words is converted
    to underscore.

    Example::

        >>> decamelize('FreshFruit')
        'fresh_fruit'

    .. note::
        This function is meant to be used with Python class names, which
        typically start with an upper-case letter. Names that start with a
        lower-case letter (e.g., 'freshFruit') will lose the first word during
        decamelization.

    """
    return '_'.join(WORD_RE.findall(s)).lower()
