Timestamp library and utility
=============================

``tslib`` is a timestamp processing toolkit and library, written in
Python. It is very helpful when dealing with the millisecond-precision
timestamps that we encounter all the time in computer systems.

Installation
------------

``tslib`` depends on ``pytz``, which you can install easily using the
provided ``requirements.txt`` file:

::

    $ pip install -r requirements.txt

You're now ready to use ``ts``. For easier access, put its directory
into your ``$PATH``:

::

    $ export PATH=`pwd`:$PATH
    $ echo "export PATH=`pwd`:\$PATH" >> ~/.bashrc     # or ~/.zshrc

Usage
-----

::

    $ ts -h
    usage: ts [-h] [-t TZ] [-n] [-i]

    Human readable timestamps

    optional arguments:
      -h, --help            show this help message and exit
      -t TZ, --timezone TZ  Use TZ as the local timezone
      -n, --timestamp-only  Only output the resulting millisecond timestamp(s)
      -i, --inline          Apply timestamp replacements inline of the incoming
                            text

``ts`` transforms milliseconds timestamps and human-readable deltas into
fully qualified date and time printouts, containing:

-  the UTC timestamp (since Epoch)
-  the UTC time represented by the timestamp
-  the local time represented by the timestamp
-  the human-readable delta of this timestamp against current time

The output is tab-delimited and can easily be re-segmented by piping
into ``column -t -s "\t"``.

Arguments can be passed as command-line arguments, or piped into ``ts``
via STDIN. If no input comes from either of these sources, ``ts`` will
simply output the current time:

::

    $ ts
    1423599084206 2015-02-10 20:11:24.206 UTC+0000  2015-02-10 12:11:24.206 PST-0800  0

Inline mode
-----------

``ts`` can operate in inline-replacement mode, for timestamps only. In
this mode, you can pipe in any text and ``ts`` will output it back to
you with all timestamps replaced with a human-readable date and time and
human-readable delta representation.

Given the inherent difficulty of accurately matching timestamps, the
matching is limited to 13-digits millisecond precision timestamps (that
may be immediately followed by a ``L``). Numbers smaller, or larger than
13 digits are not matched, and are left alone; meaning no 13-digit
section of them is matched and replaced.

::

    $ echo B_b-3PAAYAA B_cJXlvAYAA B_cJXl6AcAA \
        | xargs sfc mb g -p TSVH -f sf_checkpointTimestampMs -f sf_updatedOnMs \
        | ts -i \
        | column -t -s "    "
    sf_id        sf_checkpointTimestampMs                              sf_updatedOnMs
    B_b-3PAAYAA  2015-03-06 13:38:58.851 PST-0800 (-2w5h18m6s210)      2015-03-06 13:38:58.852 PST-0800 (-2w5h18m6s209)
    B_cJXlvAYAA  2015-03-08 09:04:36.218 PDT-0700 (-1w5d10h52m28s843)  2015-03-08 09:04:36.218 PDT-0700 (-1w5d10h52m28s844)
    B_cJXl6AcAA  2015-03-08 09:04:34.252 PDT-0700 (-1w5d10h52m30s810)  2015-03-08 09:04:34.342 PDT-0700 (-1w5d10h52m30s720)

More examples
-------------

Piping:

::

    $ cat << EOF | ts
    pipe heredoc> 1404424797009L
    pipe heredoc> 1415917836779L
    pipe heredoc> EOF
    1404424797009 2014-07-03 21:59:57.009 UTC+0000  2014-07-03 14:59:57.009 PDT-0700  -31w5d1h14m26s38
    1415917836779 2014-11-13 22:30:36.779 UTC+0000  2014-11-13 14:30:36.779 PST-0800  -12w5d43m46s268

Using the column output (assuming the same input in a ``/tmp/ts.txt``
file):

::

    $ cat /tmp/ts.txt | ts | cut -f4
    -31w5d1h16m17s703
    -12w5d45m37s933

Sorting on a column (here, by descending timestamps in first column):

::

    $ cat /tmp/ts.txt | ts | sort -k1 -t $'\t' -r
    1415917836779 2014-11-13 22:30:36.779 UTC+0000  2014-11-13 14:30:36.779 PST-0800  -12w5d46m6s924
    1404424797009 2014-07-03 21:59:57.009 UTC+0000  2014-07-03 14:59:57.009 PDT-0700  -31w5d1h16m46s694

Deltas
------

Human-readable deltas can be expressed in weeks (``w``), days (``d``),
hours (``h``), minutes (``m``), and seconds (``s``). The remainder,
without a unit, is assumed to be milliseconds. Any "segment" can be
omitted, the only requirement is that the segments that are specified
are written in descending order of span (days before hours, hours before
minutes, etc.).

Here's an example: ``-12w4d6m57s257``. Note that *hours* are missing,
which simply means 12 weeks, 4 days, 6 minutes, 57 seconds and 257
milliseconds.

As you might have guessed, deltas can be both negative and positive. For
positive deltas, the leading ``+`` may be omitted if units are used,
otherwise the number is assumed to be an absolute timestamp:

::

    $ ts -1
    1423599850752 2015-02-10 20:24:10.752 UTC+0000  2015-02-10 12:24:10.752 PST-0800  -1
    $ ts 0 1
                0 1970-01-01 00:00:00.000 UTC+0000  1969-12-31 16:00:00.000 PST-0800  -2353w5d20h24m14s145
                1 1970-01-01 00:00:00.001 UTC+0000  1969-12-31 16:00:00.001 PST-0800  -2353w5d20h24m14s144
    $ ts +1
    1423599855941 2015-02-10 20:24:15.941 UTC+0000  2015-02-10 12:24:15.941 PST-0800  1

Using a different local timezone
--------------------------------

The third column shows the timestamp's representation in local time. It
defaults to the ``US/Pacific`` timezone but this can be overridden with
the ``-t`` command-line argument, passing in a timezone name that
``pytz`` understands:

::

    $ ts -t Europe/Paris
    1423600015955 2015-02-10 20:26:55.955 UTC+0000  2015-02-10 21:26:55.955 CET+0100  0

Absolute, human-readable offsets from Epoch
-------------------------------------------

By prefixing a human-readable delta with an equal sign (``=``), you
obtain an absolute offset from the Epoch. The side-effect of this is
that it allows for converting a human-readable delta into its
corresponding millisecond duration.

::

    $ ts -n '=1h'
          3600000
    $ ts '=1d'
         86400000 1970-01-02 00:00:00.000 UTC+0000  1970-01-01 16:00:00.000 PST-0800  -2365w6d21h56m20s98


