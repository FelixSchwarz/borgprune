# -*- coding: UTF-8 -*-

from datetime import datetime as DateTime, timedelta as TimeDelta
import operator
import subprocess
import sys

from dateutil import rrule

from .archive_util import find_closest_archive, list_archives_since, list_recurring_dates
from .borg_parser import parse_borg_archive_listing


keep_config = (
    ('MONTHLY', TimeDelta(days=365)),
    ('WEEKLY', TimeDelta(days=5*30)),
    ('DAILY', TimeDelta(days=2*30)),
    ('*', TimeDelta(days=7)),
)

def calculate_archives_to_keep(keep_config, archives):
    keep_archives = set()
    if len(archives) == 0:
        return keep_archives

    now = DateTime.now()
    for frequency_str, duration in keep_config:
        start = now - duration
        if frequency_str in ('MONTHLY', 'WEEKLY', 'DAILY'):
            for datetime in list_recurring_dates(getattr(rrule, frequency_str), start, end=now):
                closest_archive = find_closest_archive(datetime, archives)
                keep_archives.add(closest_archive)
        else:
            assert frequency_str == '*'
            for newer_archive in list_archives_since(start, archives):
                keep_archives.add(newer_archive)
    # always keep the latest archive to prevent data loss
    keep_archives.add(archives[-1])
    return keep_archives

def prune_repo(borgrepo, dry_run=False, verbose=False):
    cmd = ['borg', 'list', '--json', borgrepo]
    borg_list = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    json_bytes, borg_stderr = borg_list.communicate(timeout=100)
    archives = parse_borg_archive_listing(json_bytes.decode('utf8'))

    keep_archives = calculate_archives_to_keep(keep_config, archives)
    archives_to_delete = set(archives).difference(keep_archives)
    archive_names = [archive.name for archive in sorted(archives_to_delete, key=operator.attrgetter('name'))]
    if len(archive_names) == 0:
        if verbose:
            print('no archives to delete')
        return
    elif dry_run:
        if verbose:
            print('archives to delete')
            for name in archive_names:
                print('   %s' % name)
    else:
        cmd = ['borg', 'delete', borgrepo] + archive_names
        if verbose:
            print('deleting %d archives' % len(archive_names))
        # all borg output will be redirected to the user's console as we do not configure pipes for stdout/stderr
        borg_process = subprocess.Popen(cmd, shell=False)
        return_code = borg_process.wait(timeout=None)
        if return_code != 0:
            sys.stderr.write('borg exited with error (code %r)\n' % return_code)
