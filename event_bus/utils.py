from dateutil.tz import tzlocal, tzutc
from datetime import datetime


def guess_timezone(dt):
    if _is_naive(dt):
        delta = datetime.now() - dt
        if _total_seconds(delta) < 5:
            return dt.replace(tzinfo=tzlocal())
        else:
            return dt.replace(tzinfo=tzutc())

    return dt


def _is_naive(dt):
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None


def _total_seconds(delta):
    return (delta.microseconds +
            (delta.seconds + delta.days * 24 * 3600) * 1e6) / 1e6
