# -*- coding: UTF-8 -*-

from collections import namedtuple
import json
import operator

from dateutil.parser import parse as parse_iso8601dt


__all__ = ['parse_borg_archive_listing', 'ArchiveInfo']

ArchiveInfo = namedtuple('ArchiveInfo', ('time', 'name'))

def parse_borg_archive_listing(json_bytes):
    repo_info = json.loads(json_bytes)
    archive_list = []
    for archive_data in repo_info['archives']:
        dt = parse_iso8601dt(archive_data['time'])
        name = archive_data['name']
        archive_list.append(ArchiveInfo(dt, name))
    archive_list.sort(key=operator.attrgetter('time'))
    return archive_list

