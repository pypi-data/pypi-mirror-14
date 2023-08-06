#!/usr/bin/python3 -S
# -*- coding: utf-8 -*-
"""

  `Vital HTTP Tools`
--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--·--
   The MIT License (MIT) © 2015 Marcel Hellkamp

"""
import time
import datetime


__all__ = (
  "http_date",
  "parse_date",
  "parse_auth"
)


def http_date(value):
    """ Formats the @value in required HTTP style

        @value: :class:datetime.datetime, #int, #float, #str time-like object

        -> #str HTTP-style formatted date

        ©2014, Marcel Hellkamp
    """
    if isinstance(value, datetime.datetime):
        value = value.utctimetuple()
    elif isinstance(value, (int, float)):
        value = time.gmtime(value)
    if not isinstance(value, str):
        value = time.strftime("%a, %d %b %Y %H:%M:%S GMT", value)
    return value


def parse_date(ims):
    """ Parse rfc1123, rfc850 and asctime timestamps and return UTC epoch.
        ©2014, Marcel Hellkamp
    """
    try:
        ts = email.utils.parsedate_tz(ims)
        return time.mktime(ts[:8] + (0, )) - (ts[9] or 0) - time.timezone
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def parse_auth(header):
    """ Parse rfc2617 HTTP authentication header string (basic) and return
        (user,pass) tuple or None
        ©2014, Marcel Hellkamp
    """
    try:
        method, data = header.split(None, 1)
        if method.lower() == 'basic':
            user, pwd = touni(base64.b64decode(tob(data))).split(':', 1)
            return user, pwd
    except (KeyError, ValueError):
        return None


def parse_range_header(header, maxlen=0):
    """ Yield (start, end) ranges parsed from a HTTP Range header. Skip
        unsatisfiable ranges. The end index is non-inclusive.
        ©2014, Marcel Hellkamp
    """
    if not header or header[:6] != 'bytes=': return
    ranges = [r.split('-', 1) for r in header[6:].split(',') if '-' in r]
    for start, end in ranges:
        try:
            if not start:  # bytes=-100    -> last 100 bytes
                start, end = max(0, maxlen - int(end)), maxlen
            elif not end:  # bytes=100-    -> all but the first 99 bytes
                start, end = int(start), maxlen
            else:  # bytes=100-200 -> bytes 100-200 (inclusive)
                start, end = int(start), min(int(end) + 1, maxlen)
            if 0 <= start < end <= maxlen:
                yield start, end
        except ValueError:
            pass
