import datetime

import pytest

import mediares.maze.parsers


@pytest.mark.parametrize(
    'data', [
        {
            '1': 1562326291,
            '2': 1551364282,
            '3': 1558460773,
        },
    ],
)
def test_parse_updates(data):
    parsed = mediares.maze.parsers.parse_updates(data)
    min_utc = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    max_utc = datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)
    for k, v in parsed.items():
        assert isinstance(k, int)
        assert k > 0
        assert isinstance(v, datetime.datetime)
        assert v.tzinfo is datetime.timezone.utc
        assert v > min_utc
        assert v < max_utc
