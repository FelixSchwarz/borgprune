# -*- coding: UTF-8 -*-

from datetime import datetime as DateTime

from pythonic_testcase import *

from schwarz.borgprune.borg_parser import parse_borg_archive_listing


class JSONParsingTest(PythonicTestCase):
    def test_can_parse_borg_json_with_single_archive(self):
        json_bytes = (b'{\n'
            b'"archives": [\n'
            b'        {\n'
            b'            "archive": "2016-03-31T12:34:56+0200",\n'
            b'            "barchive": "2016-03-31T12:34:56+0200",\n'
            b'            "id": "078e9bccb4f54ad9836d78bc414aba883815821075e847b898ff7769cfd9849d",\n'
            b'            "name": "2016-03-31T12:34:56+0200",\n'
            b'            "start": "2016-03-31T12:34:57.000000",\n'
            b'            "time": "2016-03-31T12:34:57.000000"\n'
            b'        }\n'
            b'    ],\n'
            b'"encryption": {\n'
            b'    "keyfile": "/home/foo/.config/borg/keys/run_user_1000_storage",\n'
            b'    "mode": "keyfile"\n'
            b'},\n'
            b'"repository": {\n'
            b'    "id": "4dd2376c6e4f45689c583dc929a36351df3a986b0a6b44448912e4080b7c66a9",\n'
            b'    "last_modified": "2017-10-24T17:19:13.000000",\n'
            b'    "location": "ssh://borg@storage.example/borg/client"\n'
            b'}\n'
            b'}\n'
        )
        archives = parse_borg_archive_listing(json_bytes)
        assert_length(1, archives)
        archive = archives[0]
        assert_equals('2016-03-31T12:34:56+0200', archive.name)
        assert_equals(DateTime(2016, 3, 31, 12, 34, 57), archive.time)

