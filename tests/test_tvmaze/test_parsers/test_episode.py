import datetime
import collections.abc

import pytest

import mediares.maze.parsers
import validators


@pytest.mark.parametrize(
    'data', [
        {
            '_links': {
                'self': {
                    'href': 'http://api.tvmaze.com/episodes/1',
                },
            },
            'airdate': '2013-06-24',
            'airstamp': '2013-06-25T02:00:00+00:00',
            'airtime': '22:00',
            'id': 1,
            'image': {
                'medium': 'http://static.tvmaze.com/uploads/images/medium_landscape/1/4388.jpg',
                'original': 'http://static.tvmaze.com/uploads/images/original_untouched/1/4388.jpg',
            },
            'name': 'Pilot',
            'number': 1,
            'runtime': 60,
            'season': 1,
            'summary': "<p>When the residents of Chester's Mill find themselves trapped under a massive transparent dome with no way out, they struggle to survive as resources rapidly dwindle and panic quickly escalates.</p>",

            'url': 'http://www.tvmaze.com/episodes/1/under-the-dome-1x01-pilot',
        }
    ],
)
def test_parse_network(data):
    known_keys = {
        'id',
        'url',
        'name',
        'season',
        'number',
        'airdate',
        'airtime',
        'airstamp',
        'runtime',
        'image',
        'summary',
        '_links',
    }
    # Make sure there were no unknown keys in the data to be parsed
    assert data is None or not known_keys.symmetric_difference(data.keys())

    expected_keys = {
        'maze_id',
        'title',
        'order',
        'air_date',
        'air_time',
        'airs',
        'runtime',
        'summary',
        'api_url',
        'web_url',
        'medium_image_url',
        'original_image_url',
    }
    parsed = mediares.maze.parsers.parse_episode(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    maze_id = parsed['maze_id']
    assert isinstance(maze_id, int)
    assert maze_id > 0

    title = parsed['title']
    assert isinstance(title, str)
    assert title

    order = parsed['order']
    assert isinstance(order, collections.abc.Iterable)
    assert not isinstance(order, str)

    season, episode = order
    assert isinstance(season, int)
    assert season >= 0

    assert isinstance(episode, int)
    assert episode > 0

    air_date = parsed['air_date']
    assert isinstance(air_date, datetime.date)
    assert not isinstance(air_date, datetime.datetime)

    air_time = parsed['air_time']
    assert isinstance(air_time, datetime.time)

    airs = parsed['airs']
    assert isinstance(airs, datetime.datetime)

    runtime = parsed['runtime']
    assert isinstance(runtime, datetime.timedelta)
    assert runtime > datetime.timedelta(minutes=0)

    summary = parsed['summary']
    assert isinstance(summary, str)
    assert summary

    assert validators.url(parsed['api_url'])
    assert validators.url(parsed['web_url'])
    assert validators.url(parsed['medium_image_url'])
    assert validators.url(parsed['original_image_url'])
