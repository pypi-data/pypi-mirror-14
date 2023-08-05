# Copyright (C) 2015 SignalFx, Inc. All rights reserved.

from __future__ import print_function

import argparse
import calendar
from datetime import datetime as dt
from datetime import timedelta as delta
import os
import pytz
import re
import sys


__author__ = 'Maxime Petazzoni <max@signalfuse.com>'
__copyright__ = 'Copyright (C) 2015 SignalFx, Inc. All rights reserved.'
__title__ = 'ts'
__version__ = '1.1'

_UNITS = {
        's': delta(seconds=1),
        'm': delta(minutes=1),
        'h': delta(hours=1),
        'd': delta(days=1),
        'w': delta(days=7),
}

_SORTED_UNITS = sorted(
    _UNITS.items(), key=lambda x: x[1], reverse=True)

_FULL_OUTPUT_FORMAT = '{ts:13d}\t{utc}.{millis:03d} {utc_tz}\t' \
        + '{local}.{millis:03d} {local_tz}\t{delta}'
_TIMESTAMP_ONLY_FORMAT = '{ts:13d}'
_LOCAL_HUMAN_FORMAT = '{local}.{millis:03d} {local_tz} ({delta})'

_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
_TZ_FORMAT = '%Z%z'

_TIMESTAMP_REGEXP = re.compile('(?<!\d)(\d{13}L?)(?!\d)')


def __timedelta_millis(td):
    """Returns the span of the given timedelta object in milliseconds."""
    return int(round(td.total_seconds(), 3) * 1000)


def utc():
    """Return a non-naive, timezone-aware datetime object representing the
    current UTC time."""
    return date_from_utc(dt.utcnow())


def date_from_utc_ts(ts):
    """Return a non-naive, timezone-aware datetime object for the UTC timezone
    representing the given millisecond-precision UTC timestamp."""
    return date_from_utc(dt.utcfromtimestamp(ts / 1000.0))


def date_from_utc(date):
    """Return a non-naive, timezone-aware datetime object for the UTC timezone
    of the given naive datetime object."""
    return pytz.utc.localize(date)


def parse_input(s):
    """Parse the given input and intelligently transform it into an absolute,
    non-naive, timezone-aware datetime object for the UTC timezone.

    The input can be specified as a millisecond-precision UTC timestamp (or
    delta against Epoch), with or without a terminating 'L'. Alternatively, the
    input can be specified as a human-readable delta string with unit-separated
    segments, like '24d6h4m500' (24 days, 6 hours, 4 minutes and 500ms), as
    long as the segments are in descending unit span order."""
    original = s

    if s[-1:] == 'L':
        s = s[:-1]

    sign = {'-': -1, '=': 0, '+': 1}.get(s[0], None)
    if sign is not None:
        s = s[1:]

    ts = 0
    for unit in _SORTED_UNITS:
        pos = s.find(unit[0])
        if pos == 0:
            raise ValueError(original)
        elif pos > 0:
            # If we find a unit letter, we're dealing with an offset. Default
            # to positive offset if a sign wasn't specified.
            if sign is None:
                sign = 1
            ts += int(s[:pos]) * __timedelta_millis(unit[1])
            s = s[min(len(s), pos + 1):]

    if s:
        ts += int(s)

    return date_from_utc_ts(ts) if not sign else \
        utc() + sign * delta(milliseconds=ts)


def parse_to_timestamp(s):
    """Parse the given input and convert to an absolute UTC timestamp since
    Epoch."""
    date = parse_input(s)
    millis = int(date.microsecond / 1000)
    ts = calendar.timegm(date.utctimetuple()) * 1000 + millis
    return ts


def render_delta(date):
    """Render the given date as a human-readable delta against Epoch."""
    d = __timedelta_millis(date - utc())
    s = '' if d >= 0 else '-'
    d = abs(d)

    for unit in _SORTED_UNITS:
        span = __timedelta_millis(unit[1])
        if d >= span:
            count = int(d // span)
            s += '{0}{1}'.format(count, unit[0])
            d -= count * span

    if d or not s:
        s += str(d)

    return s


def render_date(date, tz=pytz.utc, fmt=_FULL_OUTPUT_FORMAT):
    """Format the given date for output. The local time render of the given
    date is done using the given timezone."""
    local = date.astimezone(tz)
    millis = int(date.microsecond / 1000)
    ts = calendar.timegm(date.utctimetuple()) * 1000 + millis
    return fmt.format(
            ts=ts,
            utc=date.strftime(_DATE_FORMAT),
            millis=millis,
            utc_tz=date.strftime(_TZ_FORMAT),
            local=local.strftime(_DATE_FORMAT),
            local_tz=local.strftime(_TZ_FORMAT),
            delta=render_delta(date))


def main():
    parser = argparse.ArgumentParser(description='Human readable timestamps')
    parser.add_argument('-t', '--timezone', metavar='TZ', default='US/Pacific',
                        help='Use TZ as the local timezone')
    parser.add_argument('-n', '--timestamp-only', dest='output_format',
                        action='store_const', const=_TIMESTAMP_ONLY_FORMAT,
                        default=_FULL_OUTPUT_FORMAT,
                        help='Only output the resulting millisecond '
                             'timestamp(s)')
    parser.add_argument('-i', '--inline', dest='inline',
                        action='store_true', default=False,
                        help='Apply timestamp replacements inline '
                             'of the incoming text')
    (options, args) = parser.parse_known_args()

    tz = pytz.timezone(options.timezone)

    def render(arg, fmt):
        return render_date(parse_input(arg.strip()), tz, fmt)

    def process(arg):
        try:
            if options.inline:
                print(_TIMESTAMP_REGEXP.sub(
                        lambda m: render(m.group(0), _LOCAL_HUMAN_FORMAT),
                        arg),
                      end='')
            else:
                print(render(arg, options.output_format))
        except Exception, e:
            print('Could not parse {arg}: {error}'
                  .format(arg=arg, error=e.args[0]))
            raise

    out = False
    if len(args):
        map(process, args)
        out = True
    if not os.isatty(file.fileno(sys.stdin)):
        map(process, sys.stdin.readlines())
        out = True
    if not out:
        print(render_date(utc(), tz, options.output_format))
