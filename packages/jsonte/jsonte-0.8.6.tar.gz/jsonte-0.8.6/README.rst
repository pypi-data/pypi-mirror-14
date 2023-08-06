=============================
Jsonte (Json Type Extensions)
=============================

* Free software: Simplified BSD license

Documentation
-------------

Jsonte is just a simple and well defined way of 'extending' json to support some additional types.

The primary goal is to add support for data types that are commonly used in databases.  In particular:

* dates, times, and timestamps (both with and without timezones)
* arbitrary precision numeric entries
* binary data

A secondary goal was to do this in such a way that the resulting json was easily human readable, and
also programming language agnostic.

The format is simple, and is always itself valid json.

::

   * A date:      { "#date": "2015-05-28" }
   * A time:      { "#time": "22:12:42.381000" }
   * A timestamp: { "#tstamp": "2015-05-28T22:13:42.381000" }

These are just the ISO formats for each of the above items.

::

   * A numeric entry:  { "#num": "1234.0000" }
   * Some binary data: { "#bin": "SGVsbG8gV29ybGQhAA==" }

The numeric entry is encoded as a string so the degree of precision is not lost.
The binary data is just base64 encoded.

Key Escaping
~~~~~~~~~~~~

Keys in objects that start with either a hash (#) or a tidle (~) are escaped by a tidle (~) being prefixed to the key.
This is to avoid any accidental collisions with the 'special' object keys used.

So an object that would normaly be encoded as { "#bin": 1234 } would become { "~#bin": 1234 } when encoded by jsonte,
and { "~foo": "bar" } would become { "~~foo": "bar" }


Python Implementation
---------------------

The python implementation is designed to be a drop-in replacement for the standard json library, and is tested on
Python 2.6, 2.7 and 3.3+.

::

   import datetime
   import decimal
   import dateutil.tz
   import jsonte

   timezone = dateutil.tz.gettz('Australia/Victoria')
   data = { 'now': datetime.datetime.now(),
            'now_with_tz': datetime.datetime.now(timezone),
            'today': datetime.date.today(),
            'the_time': datetime.datetime.now().time(),
            'cost': decimal.Decimal('12.50'),
            'binary': bytearray('Hello World!\x00\x01\x02'),
            '%foo': 'a',
            '#num': 1,
            '~baz': 2.0 }

   serialiser = jsonte.JsonteSerialiser(indent=4, sort_keys=True)
   s = serialiser.dumps(data)
   data2 = serialiser.loads(s)

At this point we have

::

   >>> data is data2
   False
   >>> data == data2
   True
   >>> print s
   {
       "%foo": "a",
       "binary": {
           "#bin": "SGVsbG8gV29ybGQhAAEC"
       },
       "cost": {
           "#num": "12.50"
       },
       "now": {
           "#tstamp": "2015-05-28T23:43:40.454000"
       },
       "now_with_tz": {
           "#tstamp": "2015-05-28T23:43:40.454000+10:00"
       },
       "the_time": {
           "#time": "23:43:40.454000"
       },
       "today": {
           "#date": "2015-05-28"
       },
       "~#num": 1,
       "~~baz": 2.0
   }