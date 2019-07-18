"""Parse data from TVMaze."""

import datetime
import logging
import typing

import dateutil.tz
import pycountry

import mediares.constants

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

    name = data['name']

    by_name = pycountry.countries.get(name=name)
    log.debug(f'Country name {name!r} parses as: {by_name}')

    if by_code != by_name:
        raise ValueError(f'country is ambiguous: {by_code} != {by_name}')

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


def parse_images(data: typing.Mapping) -> typing.Mapping:
    """Parse TVMaze image urls.

    :param data: Image data from TVMaze
    :return: A mapping containing parsed image urls
    """
    return {
        'medium_image_url': data['medium'],
        'original_image_url': data['original'],
    }


def parse_link(data, key):
    """Parse a TVMaze link.

    :param data: Link data from TVMaze
    :param key: The desired link name
    :return: A url
    """
    return data[key]['href']


def parse_person(data: typing.Mapping) -> typing.Mapping:
    """Parse a TVMaze person.

    :param data: Person data from TVMaze
    :return: A mapping containing parsed person data
    """
    date_fmt = '%Y-%m-%d'

    birth = datetime.datetime.strptime(data['birthday'], date_fmt)
    birth = birth.date()

    if data['deathday']:
        death = datetime.datetime.strptime(data['deathday'], date_fmt)
        death = death.date()
    else:
        death = None

    return {
        'maze_id': data['id'],
        'name': data['name'],
        **parse_country(data['country']),
        'birth': birth,
        'death': death,
        'gender': mediares.constants.Gender[data['gender'].upper()],
        'web_url': data['url'],
        'api_url': parse_link(data['_links'], 'self'),
        **parse_images(data['image']),
    }


def parse_character(data: typing.Mapping) -> typing.Mapping:
    """Parse a TVMaze character.

    :param data: Character data from TVMaze
    :return: A mapping containing parsed character data
    """
    return {
        'maze_id': data['id'],
        'name': data['name'],
        'web_url': data['url'],
        'api_url': parse_link(data['_links'], 'self'),
        **parse_images(data['image']),
    }

def parse_episode(data: typing.Mapping) -> typing.Mapping:
    """Parse a TVMaze character.

    :param data: Character data from TVMaze
    :return: A mapping containing parsed character data
    """
    date_fmt = '%Y-%m-%d'
    time_fmt = '%H:%M'
    datetime_fmt = '%Y-%m-%dT%H:%M:%S%z'

    airdate = datetime.datetime.strptime(data['airdate'], date_fmt)
    airdate = airdate.date()

    airtime = datetime.datetime.strptime(data['airtime'], time_fmt)
    airtime = airtime.time()

    timestamp = datetime.datetime.strptime(data['airstamp'], datetime_fmt)

    return {
        'maze_id': data['id'],
        'title': data['name'],
        'order': (data['season'], data['number']),

        'air_date': airdate,
        'air_time': airtime,
        'airs': timestamp,
        'runtime': datetime.timedelta(minutes=data['runtime']),

        'summary': data['summary'],

        'api_url': parse_link(data['_links'], 'self'),
        'web_url': data['url'],
        **parse_images(data['image']),
    }
