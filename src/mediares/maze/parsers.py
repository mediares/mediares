"""Parse data from TVMaze."""

import logging
import typing

import dateutil.tz
import pycountry

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def parse_country(data: typing.Optional[typing.Mapping]) -> typing.Mapping:
    """Parse a TVMaze country.

    :param data: Country data from TVMaze
    :return: A mapping containing parsed country and timezone data
    """
    if not data:
        return {
            'country': None,
            'timezone': None,
        }

    tzname = data['timezone']
    timezone = dateutil.tz.gettz(tzname)
    log.debug(f'Timezone {tzname!r} parses as: {timezone}')

    code = data['code']

    by_code = pycountry.countries.get(alpha_2=code)
    log.debug(f'Country code {code!r} parses as: {by_code}')

    return {
        'country': by_code,
        'timezone': timezone,
    }


def parse_network(data: typing.Mapping) -> typing.Mapping:
    """Parse a TVMaze network.

    :param data: Network data from TVMaze
    :return: A mapping containing parsed network data
    """
    maze_id = data['id']
    network_name = data['name']
    return {
        'maze_id': maze_id,
        'name': network_name,
        **parse_country(data['country']),
    }


def parse_web_channel(data: typing.Mapping) -> typing.Mapping:
    """Parse a TVMaze network.

    :param data: Network data from TVMaze
    :return: A mapping containing parsed network data
    """
    return parse_network(data)
