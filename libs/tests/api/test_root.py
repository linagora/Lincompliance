#!/usr/bin/env python3

from BaseTest import BaseTest


class BasicTest(BaseTest):
    def test_launch(self) -> None:
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'Lincompliance API running', response.get_data())
