import base64
import logging
import os

import feedparser

from mpls_garbage_calendar import feed_parsing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CALENDAR_RSS_FORMAT_STRING = os.environ.get(
    'FEED_URL_FORMAT',
    'http://apps.ci.minneapolis.mn.us/CalendarApp/Ex_CalendarRSS.aspx?linkurl=http://www.ci.minneapolis.mn.us/government/calendars.asp&datebook=Garbage%20and%20Recycling%20{}%20Route%20ABE&type=rss'
)


def handler(event, context):
    logger.info(event)

    schedule_day = event['pathParameters']['schedule_day']

    feed_url = CALENDAR_RSS_FORMAT_STRING.format(schedule_day)
    logger.info('Feed URL: %s', feed_url)

    feed = feedparser.parse(feed_url)
    calendar = feed_parsing.parse_feed(feed)

    logger.info(calendar)

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": { "content-type": "text/calendar" },
        "body": base64.b64encode(calendar.to_ical())
    }

