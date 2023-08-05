# :coding: utf-8
# :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

import math
import logging

from ._version import __version__


#: `Earth's mean radius <https://en.wikipedia.org/wiki/Earth_radius#Mean_radius>`_.
EARTH_RADIUS = 6371.009


def ringfence(origin, distance, clients):
    '''Yield *clients* within *distance* of *origin* point.

    *origin* should be an instance of :class:`Point` representing the longitude
    and latitude of a point on the Earth's surface.

    *distance* should be the maximum distance in kilometres (inclusive) that
    a client can be in order to be selected.

    *clients* should be a list of :class:`Client` instances to select from
    based on distance from *origin*.

    '''
    for client in clients:
        distance_from_origin = distance_between(origin, client.location)
        if distance_from_origin <= distance:
            yield client


class Client(object):
    '''Represent a client.'''

    def __init__(self, identifier, name, location):
        '''Initialise client.

        *identifier* should be a unique identifier for the client.

        *name* should be the name of the client.

        *location* should be a :class:`Point` that represents the location of
        the client on the Earth's surface.

        '''
        self.identifier = identifier
        self.name = name
        self.location = location

    def __repr__(self):
        '''Return representation.'''
        return (
            '<Client identifier={0!r} name={1!r} point={2!r}>'
            .format(self.identifier, self.name, self.location)
        )


class Point(object):
    '''Represent a point in latitude and longitude.'''

    def __init__(self, latitude, longitude):
        '''Initialise point with *latitude* and *longitude* degrees (floats).'''
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        '''Return representation.'''
        return (
            '<Point latitude={0} longitude={1}>'
            .format(self.latitude, self.longitude)
        )


def distance_between(point_a, point_b):
    '''Return kilometres between *point_a* and *point_b* on Earth's surface.

    *point_a* and *point_b* should both be instances of :class:`Point`.

    Use `Great Circle <https://en.wikipedia.org/wiki/Great-circle_distance>`_
    formula to calculate distance.

    .. note::

        As the Earth is not perfectly spherical, the result may only be correct
        to within 0.5%.

    '''
    logger = logging.getLogger('ringfencer.distance_between')

    latitude_a = math.radians(point_a.latitude)
    longitude_a = math.radians(point_a.longitude)

    latitude_b = math.radians(point_b.latitude)
    longitude_b = math.radians(point_b.longitude)

    longitude_delta = longitude_b - longitude_a

    angle = math.acos(
        math.sin(latitude_a) * math.sin(latitude_b) +
        math.cos(latitude_a) * math.cos(latitude_b) *
        math.cos(longitude_delta)
    )
    distance = EARTH_RADIUS * angle

    logger.debug(
        'Computed distance between {0} and {1} is {2}.'
        .format(point_a, point_b, distance)
    )

    return distance
