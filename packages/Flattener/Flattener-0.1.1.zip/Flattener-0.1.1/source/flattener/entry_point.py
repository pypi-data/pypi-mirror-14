# :coding: utf-8
# :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

import logging
import argparse
import json

import flattener


def main(arguments):
    '''Command line entry point.

    *arguments* should be a list of command line arguments to parse.

    '''
    logger = logging.getLogger('flattener.entry_point.main')

    parser = argparse.ArgumentParser(description='Flatten nested lists(s).')

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

    parser.add_argument('source', help='JSON encoded list to flatten.')

    print arguments
    namespace = parser.parse_args(arguments)

    logging.basicConfig(level=logging_levels[namespace.verbosity])

    try:
        input_list = json.loads(namespace.source)

    except ValueError:
        logger.error(
            'Failed to JSON decode source value. Please fix {0!r} to be a '
            'valid JSON encoded string.'.format(namespace.source),
            exc_info=logger.isEnabledFor(logging.DEBUG)
        )

    else:
        try:
            flattened = flattener.flatten(input_list)

        except ValueError as error:
            logger.error(
                error,
                exc_info=logger.isEnabledFor(logging.DEBUG)
            )

        else:
            print flattened
