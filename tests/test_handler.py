import feedparser
import pytest
from mpls_garbage_calendar import feed_parsing


@pytest.mark.parametrize("test_input,expected", [
    ('Organics Calendar (Friday) 6/4/22 6:00 AM', None),
    ('Garbage Day 6/10/22 6:00 AM', 'Garbage'),
    ('Recycling Day 6/10/22 6:00 AM', 'Recycling')
])
def test_get_type(test_input, expected):
    assert feed_parsing.get_type(test_input) == expected


def test_parse():
    cal = feed_parsing.parse_feed(feedparser.parse(r'./Ex_CalendarRSS.aspx.xml'))

    assert len(cal.subcomponents) == 4
    assert cal.subcomponents[0]['SUMMARY'] == '\U00015FD1'
    assert cal.subcomponents[0]['DESCRIPTION'] == 'Garbage'
    assert cal.subcomponents[0]['DTSTART'].to_ical() == b'20220604'
    assert cal.subcomponents[0]['DTEND'].to_ical() == b'20220605'
    assert cal.subcomponents[1]['SUMMARY'] == '\U0000267B \U00015FD1'
    assert cal.subcomponents[1]['DESCRIPTION'] == 'Recycling, Garbage'
    assert cal.subcomponents[1]['DTSTART'].to_ical() == b'20220610'
    assert cal.subcomponents[1]['DTEND'].to_ical() == b'20220611'
