import pycountry.db
import datetime

import pytest

import mediares.maze.parsers


@pytest.mark.parametrize(
    'data', [
        {
            'country': {
                'code': 'US',
                'name': 'United States',
                'timezone': 'America/New_York',
            },
            'id': 1,
            'name': 'NBC',
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
    parsed = mediares.maze.parsers.parse_network(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    assert isinstance(parsed['maze_id'], int)
    assert parsed['maze_id'] > 0

    assert isinstance(parsed['name'], str)
    assert parsed['name']

    assert isinstance(parsed['country'], pycountry.db.Data)

    assert isinstance(parsed['timezone'], datetime.tzinfo)
