import base64
import logging
import os
import boto3

import feedparser

from mpls_garbage_calendar import feed_parsing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CALENDAR_RSS_FORMAT_STRING = os.environ.get(
    'FEED_URL_FORMAT',
    'http://apps.ci.minneapolis.mn.us/CalendarApp/Ex_CalendarRSS.aspx?linkurl=http://www.ci.minneapolis.mn.us/government/calendars.asp&datebook=Garbage%20and%20Recycling%20{}%20Route%20ABE&type=rss'
)

BUCKET_NAME = os.environ['bucket_name']


def handler(event, context):
    logger.info(event)

    schedule_day = event['pathParameters']['schedule_day']
    rss_string = event['body']

    feed = feedparser.parse(rss_string)
    calendar = feed_parsing.parse_feed(feed)

    logger.info(calendar)

    s3 = boto3.client("s3")

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=schedule_day,
        ContentType='text/calendar',
        Body=calendar.to_ical()
    )

    # calendar.to_ical()

    return "OK"
    # schedule_day = event['pathParameters']['schedule_day']
    #
    # feed_url = CALENDAR_RSS_FORMAT_STRING.format(schedule_day)
    # logger.info('Feed URL: %s', feed_url)
    #
    # feed = feedparser.parse(feed_url)
    # calendar = feed_parsing.parse_feed(feed)
    #
    # logger.info(calendar)
    #
    # return {
    #     "isBase64Encoded": True,
    #     "statusCode": 200,
    #     "headers": { "content-type": "text/calendar" },
    #     "body": base64.b64encode(calendar.to_ical())
    # }

