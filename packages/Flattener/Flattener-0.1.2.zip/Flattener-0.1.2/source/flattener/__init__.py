# :coding: utf-8
# :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

import collections

from ._version import __version__


def flatten(input_list):
    '''Return flattened copy of *input_list*.

    For example::

        >>> flatten([1, 2, [3, [4]], [5]])
        [1, 2, 3, 4, 5]


    '''
    if not isinstance(input_list, list):
        raise ValueError(
            'Cannot flatten non-list input: {0!r}'.format(input_list)
        )

    flattened = []
    stack = collections.deque(input_list)
    while stack:
        entry = stack.popleft()

        if isinstance(entry, list):
            stack.extendleft(reversed(entry))
        else:
            flattened.append(entry)

    return flattened
