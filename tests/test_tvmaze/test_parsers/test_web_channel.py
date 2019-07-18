import pycountry.db
import datetime

import pytest

import mediares.maze.parsers


@pytest.mark.parametrize(
    'data', [
        {
            'country': None,
            'id': 1,
            'name': 'Netflix',
        },
        {
            'country': {
                'code': 'US',
                'name': 'United States',
                'timezone': 'America/New_York',
            },
            'id': 2,
            'name': 'Hulu',
        },
    ],
)
def test_parse_network(data):
    known_keys = {
        'country',
        'id',
        'name',
    }
    # Make sure there were no unknown keys in the data to be parsed
    assert not known_keys.symmetric_difference(data.keys())

    expected_keys = {
        'country',
        'maze_id',
        'name',
        'timezone',
    }
    parsed = mediares.maze.parsers.parse_web_channel(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    assert isinstance(parsed['maze_id'], int)
    assert parsed['maze_id'] > 0

    assert isinstance(parsed['name'], str)
    assert parsed['name']

    country = parsed['country']
    assert country is None or isinstance(country, pycountry.db.Data)

    timezone = parsed['timezone']
    assert timezone is None or isinstance(timezone, datetime.tzinfo)

    assert (country is None and timezone is None) or (country and timezone)
