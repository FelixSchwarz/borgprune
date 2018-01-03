# -*- coding: UTF-8 -*-

from datetime import datetime as DateTime

from pythonic_testcase import *
from dateutil import rrule

from schwarz.borgprune.archive_util import find_closest_archive, list_recurring_dates
from schwarz.borgprune.borg_parser import ArchiveInfo


class ArchiveFinderTest(PythonicTestCase):
    def test_can_find_closest_archive(self):
        archives = [
            ArchiveInfo(DateTime(2016, 2, 20), 'foo'),
            ArchiveInfo(DateTime(2016, 5, 1), 'bar'),
            ArchiveInfo(DateTime(2016, 5, 30), 'baz'),
            ArchiveInfo(DateTime(2017, 1, 1), 'quox'),
        ]
        assert_equals('bar', find_closest_archive(DateTime(2016, 5, 10, hour=10, minute=25), archives).name)
        assert_equals('baz', find_closest_archive(DateTime(2016, 5, 16), archives).name)
        assert_equals('foo', find_closest_archive(DateTime(2016, 3, 1), archives).name)

    def test_can_list_recurring_monthly_dates(self):
        dates = tuple(list_recurring_dates(rrule.MONTHLY, DateTime(2016, 1, 31), DateTime(2016, 10, 31)))
        assert_length(10, dates)
        assert_equals(DateTime(2016, 1, 31), dates[0])
        assert_equals(DateTime(2016, 2, 29), dates[1])
        assert_equals(DateTime(2016, 3, 31), dates[2])
        # ...
        assert_equals(DateTime(2016, 9, 30), dates[8])
        assert_equals(DateTime(2016, 10, 31), dates[9])

    def test_can_list_recurring_daily_dates(self):
        expected = (DateTime(2016, 2, 28), DateTime(2016, 2, 29), DateTime(2016, 3, 1), DateTime(2016, 3, 2))
        dates = tuple(list_recurring_dates(rrule.DAILY, DateTime(2016, 2, 28), DateTime(2016, 3, 2)))
        assert_equals(expected, dates)
