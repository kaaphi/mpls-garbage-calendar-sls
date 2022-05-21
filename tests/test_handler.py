import feedparser
import pytest
from mpls_garbage_calendar import handler


@pytest.mark.parametrize("test_input,expected", [
    ('Organics Calendar (Friday) 6/4/22 6:00 AM', None),
    ('Garbage Day 6/10/22 6:00 AM', 'Garbage'),
    ('Recycling Day 6/10/22 6:00 AM', 'Recycling')
])
def test_get_type(test_input, expected):
    assert handler.get_type(test_input) == expected


def test_parse():
    cal = handler.parse_feed(feedparser.parse(r'./Ex_CalendarRSS.aspx.xml'))

    assert len(cal.subcomponents) == 6
    assert cal.subcomponents[0]['SUMMARY'] == 'Garbage'
    assert cal.subcomponents[0]['DTSTART'].to_ical() == b'20220604'
    assert cal.subcomponents[0]['DTEND'].to_ical() == b'20220605'
