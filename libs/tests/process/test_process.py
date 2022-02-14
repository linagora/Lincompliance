#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from shutil import copy
from unittest import TestCase

from process import Lincompliance


class LincomplianceTest(TestCase):
    def test_initialisation(self):
        lincompliance = Lincompliance('/root')
        copy("/root/libs/tests/data/hello-world-master.zip", "/tmp/hello-world-master.zip")
        lincompliance.exec("/tmp/hello-world-master.zip", "hello-world-master")
        assert True
