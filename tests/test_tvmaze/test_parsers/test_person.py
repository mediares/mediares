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
                    'href': 'http://api.tvmaze.com/people/1',
                },
            },
            'birthday': '1979-07-17',
            'country': {
                'code': 'US',
                'name': 'United States',
                'timezone': 'America/New_York',
            },
            'deathday': None,
            'gender': 'Male',
            'id': 1,
            'image': {
                'medium': 'http://static.tvmaze.com/uploads/images/medium_portrait/0/1815.jpg',
                'original': 'http://static.tvmaze.com/uploads/images/original_untouched/0/1815.jpg',
            },
            'name': 'Mike Vogel',
            'url': 'http://www.tvmaze.com/people/1/mike-vogel',
        },
        {
            '_links': {
                'self': {
                    'href': 'http://api.tvmaze.com/people/312',
                },
            },
            'birthday': '1972-08-05',
            'country': {
                'code': 'GB',
                'name': 'United Kingdom',
                'timezone': 'Europe/London',
            },
            'deathday': '2015-01-14',
            'gender': 'Male',
            'id': 312,
            'image': {
                'medium': 'http://static.tvmaze.com/uploads/images/medium_portrait/2/6895.jpg',
                'original': 'http://static.tvmaze.com/uploads/images/original_untouched/2/6895.jpg',
            },
            'name': 'Darren Shahlavi',
            'url': 'http://www.tvmaze.com/people/312/darren-shahlavi',
        },
    ],
)
def test_parse_person(data):
    known_keys = {
        '_links',
        'birthday',
        'country',
        'deathday',
        'gender',
        'id',
        'image',
        'name',
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
        'gender',
        'birth',
        'death',
        'country',
        'timezone',
    }
    parsed = mediares.maze.parsers.parse_person(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    maze_id = parsed['maze_id']
    assert isinstance(maze_id, int)
    assert maze_id > 0

    name = parsed['name']
    assert isinstance(name, str)
    assert name

    birth = parsed['birth']
    assert isinstance(birth, datetime.date)
    assert not isinstance(birth, datetime.datetime)

    death = parsed['death']
    assert death is None or isinstance(death, datetime.date)
    assert death is None or not isinstance(death, datetime.datetime)

    assert isinstance(parsed['country'], pycountry.db.Data)
    assert isinstance(parsed['timezone'], datetime.tzinfo)

    assert parsed['gender'] in mediares.constants.Gender

    assert validators.url(parsed['api_url'])
    assert validators.url(parsed['web_url'])
    assert validators.url(parsed['medium_image_url'])
    assert validators.url(parsed['original_image_url'])
