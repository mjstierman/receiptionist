""" Utility functions for time handling and formatting. """

import logging

from datetime import datetime
from zoneinfo import ZoneInfo

def append_timezone(dt_str, tz_str):
    """ Append timezone information to a datetime string. """
    try:
        logging.info("Appending timezone: %s to datetime: %s", tz_str, dt_str)
        dt = datetime.fromisoformat(dt_str)
        tz = ZoneInfo(tz_str)
        dt = dt.replace(tzinfo=tz)
        return dt.isoformat()
    except Exception as e:
        logging.error("Error appending timezone: %s", e)
        return None

def to_UTC(dt_str):
    """ Convert a timezone-aware datetime string to UTC. """
    try:
        logging.info("Converting to UTC: %s", dt_str)
        dt = datetime.fromisoformat(dt_str)
        dt_utc = dt.astimezone(ZoneInfo('UTC'))
        return dt_utc.isoformat()
    except Exception as e:
        logging.error("Error converting to UTC: %s", e)
        return None