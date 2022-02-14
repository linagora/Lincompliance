#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytest import mark

from common.strings import has_ext


@mark.parametrize("filename, extensions, expected",
                  [("test.zip", ['zip'], True),
                   ("test.nop", ['zip'], False),
                   ("test", ['test'], False),
                   ("test.yep", ['zip', 'yep', 'mam'], True),
                   ("test.nop", ['zip', 'yep', 'mam'], False)])
def test_has_ext(filename, extensions, expected):
    assert has_ext(filename, extensions) == expected
