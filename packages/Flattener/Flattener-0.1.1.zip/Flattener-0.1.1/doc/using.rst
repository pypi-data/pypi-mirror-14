..
    :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

.. _using:

*****
Using
*****

Flattener provides support for flattening arbitrarily nested lists of lists.

It can be used either directly from the command line or as a library.

.. _using/command_line:

Command line
============

Run the package using Python and pass a JSON encoded string that represents the
list to flatten:

.. code-block:: console

    $ python -m flattener "[1, 2, [3, [4], 5]]"
    [1, 2, 3, 4, 5]

The program will print the flattened result.

If the input is not valid JSON an error will be logged:

.. code-block:: console

    $ python -m flattener "[1, 2, [3, [4],]]"
    ERROR:flattener.entry_point.main:Failed to JSON decode source value.
    Please fix '[1, 2, [3, [4],]]' to be a valid JSON encoded string.

Equally, if the input is not a list an error will be logged:

.. code-block:: console

    $ python -m flattener 42
    ERROR:flattener.entry_point.main:Cannot flatten non-list input: 42

.. _using/library:

Library
=======

To use as a library simply import the package::

    >>> import flattener

and call the :func:`~flattener.flatten` function::

    >>> flattener.flatten([1, 2, [3, [4], 5]])
    [1, 2, 3, 4, 5]

Invalid input values will raise a :exc:`ValueError`::

    >>> flattener.flatten(42)
    ValueError: Cannot flatten non-list input: 42
