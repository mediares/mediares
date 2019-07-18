import pycountry.db
import datetime

import pytest

import mediares.maze.parsers


@pytest.mark.parametrize(
    'data', [
        None,
        {
            'code': 'US',
            'name': 'United States',
            'timezone': 'America/New_York',
        },
        pytest.param(
            {
                'code': 'US',
                'name': 'Brazil',
                'timezone': 'America/New_York',
            },
            marks=pytest.mark.xfail(
                raises=ValueError,
                reason='Code and name do not parse equal',
            ),
        ),
    ],
)
def test_parse_network(data):
    known_keys = {
        'code',
        'name',
        'timezone',
    }
    # Make sure there were no unknown keys in the data to be parsed
    assert data is None or not known_keys.symmetric_difference(data.keys())

    expected_keys = {
        'country',
        'timezone',
    }
    parsed = mediares.maze.parsers.parse_country(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    country = parsed['country']
    assert country is None or isinstance(country, pycountry.db.Data)

    timezone = parsed['timezone']
    assert timezone is None or isinstance(timezone, datetime.tzinfo)

    assert (country is None and timezone is None) or (country and timezone)
