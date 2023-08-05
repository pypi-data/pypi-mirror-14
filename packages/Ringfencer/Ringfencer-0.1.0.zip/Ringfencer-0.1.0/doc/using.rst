..
    :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

.. _using:

*****
Using
*****

Ringfencer allows quickly determining clients that are within range of a given
location.

It can be used either directly from the command line or as a library.

.. _using/command_line:

Command line
============

Run the package using Python passing the origin location in latitude and
longitude, a file containing a list of clients to select from and an optional
max distance.

The program will then output a list of clients, sorted by identifier, that fall
within the given range of the origin location.

.. code-block:: console

    $ python -m ringfencer 52.4 -2.25 clients.txt --distance 10
    13 Simon Lenkin
    54 Julia Childs
    56 Joe Daggio
    98 Melissa Strong

The client list should be a file containing a list of clients, one per line,
with each client a JSON encoded mapping. See
:func:`ringfencer.entry_point.convert_data_to_client` for details on format.

Any issues encountered parsing the entries will be logged as warnings.

Use the *help* flag to see all options:

.. code-block:: console

    $ python -m ringfencer --help

.. _using/library:

Library
=======

To use as a library first import the package::

    >>> import ringfencer

Then construct the origin :class:`~ringfencer.Point` to measure from::

    >>> origin = ringfencer.Point(52.4, -2.25)

And assemble a list of :class:`~ringfencer.Client` instances to select from::

    >>> clients = [
        ringfencer.Client(
            identifier=1,
            name='Bob Presido',
            location=ringfencer.Point(52.46, -1.7)
        ),
        ringfencer.Client(
            identifier=2,
            name='Sarah Long',
            location=ringfencer.Point(34.46, -2.1)
        )
    ]

Then call the :func:`~ringfencer.ringfence` function iterating over the
yielded matching clients::

    >>> for client in ringfencer.ringfence(origin, 100, clients):
    >>>     print client.name
    Bob Presido

To explicitly measure the distance between two points use the
:func:`~ringfencer.distance_between` function:

    >>> print ringfencer.distance_between(origin, clients[0].location)
    37.8814922002
