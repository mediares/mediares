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
    expected_keys = {
        'country',
        'maze_id',
        'name',
        'timezone',
    }
    parsed = mediares.maze.parsers.parse_network(data)

    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())
