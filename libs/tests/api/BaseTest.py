#!/usr/bin/env python3

from unittest import TestCase, mock

from api import app


class BaseTest(TestCase):
    @mock.patch('process.Lincompliance')
    def setUp(self, mocker) -> None:
        self.app = app.test_client()
