#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import mock
from pytest import mark

from common.file import path_has_extension


@mark.parametrize('extension, expected', [
    ('conf', True),
    ('test', False),
    ('.zip', True)
])
def test_has_extension(extension: str, expected: bool) -> None:
    with mock.patch('common.file.listdir') as mocker:
        mocker.return_value = ['alpha', 'file.conf', 'file.zip', 'beta', 'project.conf']
        assert path_has_extension('.', extension) == expected

