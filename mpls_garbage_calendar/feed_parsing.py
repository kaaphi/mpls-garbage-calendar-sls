import datetime
import itertools
import re
import uuid
from typing import Optional

import feedparser
from icalendar import Calendar, Event


def parse_feed(feed: feedparser.FeedParserDict):
    cal = Calendar()

    for e in build_events(filter(None, map(parse_entry, feed.entries))):
        cal.add_component(e)

    return cal


def build_events(events):
    def date_key(e): return e['date']

    return map(build_event, itertools.groupby(sorted(events, key=date_key), date_key))


def build_event(tuple):
    (date, pickup_events) = tuple
    end_date = date + datetime.timedelta(days=1)

    event = Event()
    event.add('uid', uuid.uuid4())
    event.add('summary', ", ".join(map(lambda e: e['type'], pickup_events)))
    event.add('dtstart', date)
    event.add('dtend', end_date)

    return event


def parse_entry(entry: dict) -> Optional[dict]:
    """ Parse an RSS feed entry into a simple type and date dict or None if the entry doesn't match """
    event_type = get_type(entry.title)
    if not event_type:
        return None

    published = entry.published_parsed
    date = datetime.date(published.tm_year, published.tm_mon, published.tm_mday)

    return {
        'type': event_type,
        'date': date
    }


def get_type(title: str) -> Optional[str]:
    """ Extract the type (Garbage or Recycling) or None if none match """
    return next(
        filter(None,
               map(
                   lambda event_type: event_type if re.search(event_type, title, re.IGNORECASE) else None,
                   ['Garbage', 'Recycling']
               )),
        None)
