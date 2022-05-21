import datetime
import logging
import re
import uuid
from typing import Optional

import feedparser
from icalendar import Event, Calendar

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    logger.info(context)

    return {}


def parse_feed(feed: feedparser.FeedParserDict):
    cal = Calendar()

    for e in filter(None, map(parse_entry, feed.entries)):
        cal.add_component(e)

    return cal


def parse_entry(entry: dict) -> Optional[Event]:
    event_type = get_type(entry.title)
    if not event_type:
        return None

    published = entry.published_parsed
    start_date = datetime.date(published.tm_year, published.tm_mon, published.tm_mday)
    end_date = start_date + datetime.timedelta(days=1)

    event = Event()
    event.add('uid', uuid.uuid4())
    event.add('summary', event_type)
    event.add('dtstart', start_date)
    event.add('dtend', end_date)

    return event


def get_type(title: str) -> Optional[str]:
    return next(
        filter(None,
               map(
                   lambda event_type: event_type if re.search(event_type, title, re.IGNORECASE) else None,
                   ['Garbage', 'Recycling']
               )),
        None)