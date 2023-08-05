====================================================
dateparser -- python parser for human readable dates
====================================================

.. image:: https://img.shields.io/travis/scrapinghub/dateparser/master.svg?style=flat-square
    :target: https://travis-ci.org/scrapinghub/dateparser
    :alt: travis build status

.. image:: https://img.shields.io/pypi/dd/dateparser.svg?style=flat-square
    :target: https://pypi.python.org/pypi/dateparser/
    :alt: pypi downloads per day

.. image:: https://img.shields.io/pypi/v/dateparser.svg?style=flat-square
    :target: https://pypi.python.org/pypi/dateparser
    :alt: pypi version


`dateparser` provides modules to easily parse localized dates in almost
any string formats commonly found on web pages.


Documentation
=============

Documentation can be found `here <https://dateparser.readthedocs.org/en/latest/>`_.


Features
========

* Generic parsing of dates in English, Spanish, Dutch, Russian and several other languages and formats.
* Generic parsing of relative dates like: ``'1 min ago'``, ``'2 weeks ago'``, ``'3 months, 1 week and 1 day ago'``.
* Generic parsing of dates with time zones abbreviations or UTC offsets like: ``'August 14, 2015 EST'``, ``'July 4, 2013 PST'``, ``'21 July 2013 10:15 pm +0500'``.
* Support for non-Gregorian calendar systems. See `Supported Calendars`_. 
* Extensive test coverage.


Usage
=====

The most straightforward way is to use the `dateparser.parse <#dateparser.parse>`_ function,
that wraps around most of the functionality in the module.





Popular Formats
---------------

    >>> import dateparser
    >>> dateparser.parse('12/12/12')
    datetime.datetime(2012, 12, 12, 0, 0)
    >>> dateparser.parse(u'Fri, 12 Dec 2014 10:55:50')
    datetime.datetime(2014, 12, 12, 10, 55, 50)
    >>> dateparser.parse(u'Martes 21 de Octubre de 2014')  # Spanish (Tuesday 21 October 2014)
    datetime.datetime(2014, 10, 21, 0, 0)
    >>> dateparser.parse(u'Le 11 Décembre 2014 à 09:00')  # French (11 December 2014 at 09:00)
    datetime.datetime(2014, 12, 11, 9, 0)
    >>> dateparser.parse(u'13 января 2015 г. в 13:34')  # Russian (13 January 2015 at 13:34)
    datetime.datetime(2015, 1, 13, 13, 34)
    >>> dateparser.parse(u'1 เดือนตุลาคม 2005, 1:00 AM')  # Thai (1 October 2005, 1:00 AM)
    datetime.datetime(2005, 10, 1, 1, 0)

This will try to parse a date from the given string, attempting to
detect the language each time.

You can specify the language(s), if known, using ``languages`` argument. In this case, given languages are used and language detection is skipped:

    >>> dateparser.parse('2015, Ago 15, 1:08 pm', languages=['pt', 'es'])
    datetime.datetime(2015, 8, 15, 13, 8)

If you know the possible formats of the dates, you can
use the ``date_formats`` argument:

    >>> dateparser.parse(u'22 Décembre 2010', date_formats=['%d %B %Y'])
    datetime.datetime(2010, 12, 22, 0, 0)


Relative Dates
--------------

    >>> parse('1 hour ago')
    datetime.datetime(2015, 5, 31, 23, 0)
    >>> parse(u'Il ya 2 heures')  # French (2 hours ago)
    datetime.datetime(2015, 5, 31, 22, 0)
    >>> parse(u'1 anno 2 mesi')  # Italian (1 year 2 months)
    datetime.datetime(2014, 4, 1, 0, 0)
    >>> parse(u'yaklaşık 23 saat önce')  # Turkish (23 hours ago)
    datetime.datetime(2015, 5, 31, 1, 0)
    >>> parse(u'Hace una semana')  # Spanish (a week ago)
    datetime.datetime(2015, 5, 25, 0, 0)
    >>> parse(u'2小时前')  # Chinese (2 hours ago)
    datetime.datetime(2015, 5, 31, 22, 0)

.. note:: Testing above code might return different values for you depending on your environment's current date and time.


Dependencies
============

`dateparser` relies on following libraries in some ways:

  * dateutil_'s module ``parser`` to parse the translated dates.
  * PyYAML_ for reading language and configuration files.
  * jdatetime_ to convert *Jalali* dates to *Gregorian*.
  * umalqurra_ to convert *Hijri* dates to *Gregorian*.

.. _dateutil: https://pypi.python.org/pypi/python-dateutil
.. _PyYAML: https://pypi.python.org/pypi/PyYAML
.. _jdatetime: https://pypi.python.org/pypi/jdatetime
.. _umalqurra: https://pypi.python.org/pypi/umalqurra/


Supported languages
===================

* Arabic
* Belarusian
* Chinese
* Czech
* Dutch
* English
* Filipino
* Finnish
* French
* German
* Indonesian
* Italian
* Persian
* Polish
* Portuguese
* Romanian
* Russian
* Spanish
* Thai
* Turkish
* Ukrainian
* Vietnamese


Supported Calendars
===================
* Gregorian calendar.

* Persian Jalali calendar. For more information, refer to `Persian Jalali Calendar <https://en.wikipedia.org/wiki/Iranian_calendars#Zoroastrian_calendar>`_.

* Hijri/Islamic Calendar. For more information, refer to `Hijri Calendar <https://en.wikipedia.org/wiki/Islamic_calendar>`_.

	>>> from dateparser.calendars.jalali import JalaliParser
	>>> JalaliParser(u'جمعه سی ام اسفند ۱۳۸۷').get_date()
	datetime.datetime(2009, 3, 20, 0, 0)

        >>> from dateparser.calendars.hijri import HijriCalendar
        >>> HijriCalendar(u'17-01-1437 هـ 08:30 مساءً').get_date()
        {'date_obj': datetime.datetime(2015, 10, 30, 20, 30), 'period': 'day'}

.. note:: `HijriCalendar` has some limitations with Python 3.
.. note:: For `Finnish` language, please specify `settings={'SKIP_TOKENS': []}` to correctly parse freshness dates.


.. :changelog:

History
=======

0.3.3 (2016-02-29)
------------------
New features:

* Finnish language support.

Improvements:

* Faster parsing with switching to regex module.
* `RETURN_AS_TIMEZONE_AWARE` setting to return tz aware date object.
* Fixed conflicts with month/weekday names similarity across languages.

0.3.2 (2016-01-25)
------------------
New features:

* Added Hijri Calendar support.
* Added settings for better control over parsing dates.
* Support to convert parsed time to the given timezone for both complete and relative dates.

Improvements:

* Fixed problem with caching `datetime.now` in `FreshnessDateDataParser`.
* Added month names and week day names abbreviations to several languages.
* More simplifications for Russian and Ukranian languages.
* Fixed problem with parsing time component of date strings with several kinds of apostrophes.


0.3.1 (2015-10-28)
------------------
New features:

* Support for Jalali Calendar.
* Belarusian language support.
* Indonesian language support.


Improvements:

* Extended support for Russian and Polish.
* Fixed bug with time zone recognition.
* Fixed bug with incorrect translation of "second" for Portuguese.


0.3.0 (2015-07-29)
------------------
New features:

* Compatibility with Python 3 and PyPy.

Improvements:

* `languages.yaml` data cleaned up to make it human-readable.
* Improved Spanish date parsing.


0.2.1 (2015-07-13)
------------------
* Support for generic parsing of dates with UTC offset.
* Support for Filipino dates.
* Improved support for French and Spanish dates.


0.2.0 (2015-06-17)
------------------
* Easy to use `parse` function
* Languages definitions using YAML.
* Using translation based approach for parsing non-english languages. Previously, `dateutil.parserinfo` was used for language definitions.
* Better period extraction.
* Improved tests.
* Added a number of new simplifications for more comprehensive generic parsing.
* Improved validation for dates.
* Support for Polish, Thai and Arabic dates.
* Support for `pytz` timezones.
* Fixed building and packaging issues.


0.1.0 (2014-11-24)
------------------

* First release on PyPI.


