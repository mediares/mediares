import datetime

import pycountry.db
import pytest
import validators

import mediares.maze.parsers


@pytest.mark.parametrize(
    'data', [
        {
            '_links': {
                'self': {
                    'href': 'http://api.tvmaze.com/seasons/1',
                },
            },
            'endDate': '2013-09-16',
            'episodeOrder': 13,
            'id': 1,
            'image': {
                'medium': 'http://static.tvmaze.com/uploads/images/medium_portrait/24/60941.jpg',
                'original': 'http://static.tvmaze.com/uploads/images/original_untouched/24/60941.jpg',
            },
            'name': '',
            'network': {
                'country': {
                    'code': 'US',
                    'name': 'United States',
                    'timezone': 'America/New_York',
                },
                'id': 2,
                'name': 'CBS',
            },
            'number': 1,
            'premiereDate': '2013-06-24',
            'summary': '',
            'url': 'http://www.tvmaze.com/seasons/1/under-the-dome-season-1',
            'webChannel': None,
        },
        {
            '_links': {
                'self': {
                    'href': 'http://api.tvmaze.com/seasons/116',
                },
            },
            'endDate': '2013-04-19',
            'episodeOrder': 13,
            'id': 116,
            'image': {
                'medium': 'http://static.tvmaze.com/uploads/images/medium_portrait/59/149429.jpg',
                'original': 'http://static.tvmaze.com/uploads/images/original_untouched/59/149429.jpg',
            },
            'name': '',
            'network': None,
            'number': 1,
            'premiereDate': '2013-04-19',
            'summary': None,
            'url': 'http://www.tvmaze.com/seasons/116/hemlock-grove-season-1',
            'webChannel': {
                'country': None,
                'id': 1,
                'name': 'Netflix',
            },
        },
    ],
)
def test_parse_network(data):
    known_keys = {
        'id',
        'url',
        'number',
        'name',
        'episodeOrder',
        'premiereDate',
        'endDate',
        'network',
        'webChannel',
        'image',
        'summary',
        '_links',
    }
    # Make sure there were no unknown keys in the data to be parsed
    assert data is None or not known_keys.symmetric_difference(data.keys())

    expected_keys = {
        'maze_id',
        'title',
        'season_number',
        'episodes_ordered',
        'start_date',
        'end_date',
        'summary',
        'network',
        'web_channel',
        'api_url',
        'web_url',
        'medium_image_url',
        'original_image_url',
    }
    parsed = mediares.maze.parsers.parse_season(data)
    # Make sure all expected keys exist in parsed result
    assert not expected_keys.symmetric_difference(parsed.keys())

    maze_id = parsed['maze_id']
    assert isinstance(maze_id, int)
    assert maze_id > 0

    season_number = parsed['season_number']
    assert isinstance(season_number, int)
    assert season_number >= 0

    title = parsed['title']
    assert isinstance(title, str)
    assert title.strip() or not title

    ordered = parsed['episodes_ordered']
    assert isinstance(ordered, int)
    assert ordered > 0

    start_date = parsed['start_date']
    assert isinstance(start_date, datetime.date)
    assert not isinstance(start_date, datetime.datetime)

    end_date = parsed['end_date']
    assert isinstance(end_date, datetime.date)
    assert not isinstance(end_date, datetime.datetime)

    summary = parsed['summary']
    assert isinstance(summary, str)
    assert summary.strip() or not summary

    assert validators.url(parsed['api_url'])
    assert validators.url(parsed['web_url'])
    assert validators.url(parsed['medium_image_url'])
    assert validators.url(parsed['original_image_url'])

    network = parsed['network']
    if network:
        expected_network_keys = {
            'country',
            'maze_id',
            'name',
            'timezone',
        }
        # Make sure all expected keys exist in parsed result
        assert not expected_network_keys.symmetric_difference(network.keys())

        assert isinstance(network['maze_id'], int)
        assert network['maze_id'] > 0

        assert isinstance(network['name'], str)
        assert network['name']

        assert isinstance(network['country'], pycountry.db.Data)

        assert isinstance(network['timezone'], datetime.tzinfo)

    web_channel = parsed['web_channel']
    if web_channel:
        expected_web_channel_keys = {
            'country',
            'maze_id',
            'name',
            'timezone',
        }
        # Make sure all expected keys exist in parsed result
        assert not expected_web_channel_keys.symmetric_difference(
            web_channel.keys()
        )

        assert isinstance(web_channel['maze_id'], int)
        assert web_channel['maze_id'] > 0

        assert isinstance(web_channel['name'], str)
        assert web_channel['name']

        country = web_channel['country']
        assert country is None or isinstance(country, pycountry.db.Data)

        timezone = web_channel['timezone']
        assert timezone is None or isinstance(timezone, datetime.tzinfo)

        assert (country is None and timezone is None) or (country and timezone)
