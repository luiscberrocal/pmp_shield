import datetime
from unittest import mock
import os

import pytz
from django.test import TestCase
from ..utils import Timer, add_date_to_filename
import logging
logger = logging.getLogger(__name__)
__author__ = 'lberrocal'


class MockPerfCounter(object):

    def __init__(self):
        self.t = 0

    def increment(self, n):
        self.t += n

    def perf_counter(self):
        return self.t


class TestTimer(TestCase):


    def test_get_elapsed_time_str(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            #clock.increment(3600.0)
            stopwatch = Timer()
            stopwatch.start()
            clock.increment(120.5)
            stopwatch.stop()
            self.assertEqual('0 h 2 m 0.50 s', stopwatch.get_elapsed_time_str())

    def test_get_elapsed_time_str_with(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            #clock.increment(3600.0)
            with Timer() as stopwatch:
                clock.increment(360.25)
            self.assertEqual('0 h 6 m 0.25 s', stopwatch.get_elapsed_time_str())


class TestAddDateToFilename(TestCase):

    def setUp(self):
        self.mock_datetime = pytz.timezone('America/Panama').localize(
            datetime.datetime.strptime('2016-07-07 16:40', '%Y-%m-%d %H:%M'))


    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos_20160707_1640.txt', new_filename)

        filename = r'c:\kilo\poli\namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos.nemo_20160707_1640.txt', new_filename)

        filename = r'/my/linux/path/namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'/my/linux/path/namos.nemo_20160707_1640.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_preffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'c:\kilo\poli\20160707_1640_namos.txt', new_filename)

        filename = r'/my/linux/path/namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'/my/linux/path/20160707_1640_namos.txt', new_filename)


    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_filename(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'namos.txt'
        new_filename = add_date_to_filename(filename)
        self.assertEqual('namos_20160707_1640.txt', new_filename)
