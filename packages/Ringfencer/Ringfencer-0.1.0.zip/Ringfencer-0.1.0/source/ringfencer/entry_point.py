# :coding: utf-8
# :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

import logging
import operator
import argparse
import json

import ringfencer


def convert_data_to_client(data):
    '''Return :class:`ringfencer.Client` instance built from *data* mapping.

    *data* should contain the following:

        :user_id: The unique identifier of the client.
        :name: The name of the client.
        :latitude: The latitude of the clients position on Earth's surface.
        :longitude: The longitude of the clients position on Earth's surface.

    Raise :exc:`ValueError` if *data* is invalid.

    '''
    processed_data = {}
    for field in ('user_id', 'name', 'latitude', 'longitude'):
        if field not in data:
            raise ValueError('Missing required field {0!r}.'.format(field))

        value = data[field]
        if not value:
            raise ValueError('{0!r} field value cannot be null.'.format(field))

        if field in ('latitude', 'longitude'):
            try:
                value = float(value)
            except ValueError:
                raise ValueError(
                    '{0!r} field value {1!r} could not be converted to a float.'
                    .format(field, value)
                )

        processed_data[field] = value

    return ringfencer.Client(
        identifier=processed_data['user_id'],
        name=processed_data['name'],
        location=ringfencer.Point(
            latitude=processed_data['latitude'],
            longitude=processed_data['longitude']
        )
    )


def load_clients_from_file(file_handler, on_error=None):
    '''Yield :class:`ringfencer.Client` instances loaded from *file_handler*.

    Parse each line of the file as JSON and attempt to convert into a valid
    :class:`ringfencer.Client` instance using :func:`convert_data_to_client`.

    If *on_error* is not specified then errors will be logged as warnings, but
    otherwise ignored. Specify *on_error* as a callable to have that callable
    called with any errors that occur.

    '''
    logger = logging.getLogger('ringfencer.entry_point.load_clients_from_file')

    for line in file_handler:
        logger.debug(u'Processing {0!r}'.format(line))

        # Process as JSON.
        try:
            client_data = json.loads(line)

        except ValueError as error:
            logger.warning(
                u'Could not covert line into client as not valid JSON: {0!r}'
                .format(line)
            )
            if on_error:
                on_error(error)

            continue

        # Convert to :class:`Client` instance.
        try:
            client = convert_data_to_client(client_data)

        except ValueError as error:
            logger.warning(
                u'Invalid client data: {0!r}. {1}'
                .format(client_data, error)
            )

            if on_error:
                on_error(error)

            continue

        # Yield valid client instance.
        yield client


def main(arguments):
    '''Command line entry point.

    *arguments* should be a list of command line arguments to parse.

    '''
    logger = logging.getLogger('ringfencer.entry_point.main')

    parser = argparse.ArgumentParser(
        description=(
            'Determine which clients are located within a certain range of '
            'a specified point on the Earth\'s surface (so that you can invite'
            'them round for food and drink).'
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Allow setting of logging level from arguments.
    logging_levels = {}
    for level in (
        logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING,
        logging.ERROR, logging.CRITICAL
    ):
        logging_levels[logging.getLevelName(level).lower()] = level

    parser.add_argument(
        '-v', '--verbosity',
        help='Set the logging output verbosity.',
        choices=logging_levels.keys(),
        default='info'
    )

    # Add as separate arguments due to http://bugs.python.org/issue14074
    parser.add_argument(
        'latitude',
        type=float,
        help='Latitude in degrees (float) of origin point.'
    )
    parser.add_argument(
        'longitude',
        type=float,
        help='Longitude in degrees (float) of origin point.'
    )
    parser.add_argument(
        'clients',
        help='Path to a file that contains clients to select from.',
        type=file
    )
    parser.add_argument(
        '--distance',
        help=(
            'Distance in kilometres (inclusive) that candidates must be within '
            'in order to be selected.'
        ),
        type=float,
        default=100
    )

    namespace = parser.parse_args(arguments)

    logging.basicConfig(level=logging_levels[namespace.verbosity])

    origin = ringfencer.Point(
        namespace.latitude, namespace.longitude
    )

    selected = list(
      ringfencer.ringfence(
          origin=origin,
          distance=namespace.distance,
          clients=load_clients_from_file(namespace.clients)
      )
    )

    for client in sorted(selected, key=operator.attrgetter('identifier')):
        print (
            '{0.identifier} {0.name}'.format(client)
        )
