import datetime

import pycountry
import pytest
import validators

import mediares.constants
import mediares.maze.parsers


@pytest.mark.parametrize(
    'data', [
        {
            '_links': {
                'self': {
                    'href': 'http://api.tvmaze.com/characters/1',
                },
            },
            'id': 1,
            'image': {
                'medium': 'http://static.tvmaze.com/uploads/images/medium_portrait/0/3.jpg',
                'original': 'http://static.tvmaze.com/uploads/images/original_untouched/0/3.jpg',
            },
            'name': 'Dale "Barbie" Barbara',
            'url': 'http://www.tvmaze.com/characters/1/under-the-dome-dale-barbie-barbara',
        },
    ],
)
def test_parse_person(data):
    known_keys = {
        '_links',
        'name',
        'id',
        'image',
        'url',
    }
    # Make sure there were no unknown keys in the data to be parsed
    assert not known_keys.symmetric_difference(data.keys())

    expected_keys = {
        'maze_id',
        'name',
        'api_url',
        'web_url',
        'medium_image_url',
        'original_image_url',
    }
    parsed = mediares.maze.parsers.parse_character(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    maze_id = parsed['maze_id']
    assert isinstance(maze_id, int)
    assert maze_id > 0

    name = parsed['name']
    assert isinstance(name, str)
    assert name

    assert validators.url(parsed['api_url'])
    assert validators.url(parsed['web_url'])
    assert validators.url(parsed['medium_image_url'])
    assert validators.url(parsed['original_image_url'])
