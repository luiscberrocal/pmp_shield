import calendar
import datetime
import json
import os
from django.conf import settings
import pytz
from django.utils import timezone
from datetime import datetime, date, timedelta
import time

__author__ = 'lberrocal'


def create_output_filename_with_date(filename):
    if not os.path.exists(settings.TEST_OUTPUT_PATH):
        os.makedirs(settings.TEST_OUTPUT_PATH)
    return add_date_to_filename(os.path.join(settings.TEST_OUTPUT_PATH, filename))

def add_date_to_filename(filename, **kwargs):
    new_filename = dict()
    #path_parts = filename.split(os.path.se)
    if '/' in filename and '\\' in filename:
        raise ValueError('Filename %s contains both / and \\ separators' % filename)
    if '\\' in filename:
        path_parts = filename.split('\\')
        file = path_parts[-1]
        path = '\\'.join(path_parts[:-1])
        separator = '\\'
    elif '/' in filename:
        path_parts = filename.split('/')
        file = path_parts[-1]
        path = '/'.join(path_parts[:-1])
        separator = '/'
    else:
        file=filename
        path = ''
        separator = ''

    new_filename['path'] = path
    parts = file.split('.')
    new_filename['extension'] = parts[-1]
    new_filename['separator'] = separator
    new_filename['filename_with_out_extension'] = '.'.join(parts[:-1])
    new_filename['datetime'] = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M')
    date_position = kwargs.get('date_position', 'suffix')
    if date_position=='suffix':
        return '{path}{separator}{filename_with_out_extension}_{datetime}.{extension}'.format(**new_filename)
    else:
        return '{path}{separator}{datetime}_{filename_with_out_extension}.{extension}'.format(**new_filename)





class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def force_date_to_datetime(unconverted_date, tzinfo= pytz.UTC):
    converted_datetime = date(year=unconverted_date.year,
                              month=unconverted_date.month,
                              day=unconverted_date.day,
                              hour=0,
                              minute=0,
                              second=0,
                              tzinfo=tzinfo)
    return converted_datetime


class Timer:
    def __init__(self):
        self.elapsed = 0.0
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = time.perf_counter()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = time.perf_counter()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    def get_elapsed_time(self):
        hours, remainder = divmod(self.elapsed, 3600)
        mins, secs = divmod(remainder, 60)
        return int(hours), int(mins), secs

    def get_elapsed_time_str(self):
        return '%d h %d m %.2f s' % self.get_elapsed_time()

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def load_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def datetime_to_local_time(date_time):
    time_zone = pytz.timezone(settings.TIME_ZONE)
    return date_time.astimezone(time_zone)
