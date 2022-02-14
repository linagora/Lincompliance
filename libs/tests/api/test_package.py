#!/usr/bin/env python3
from json import loads
from io import BytesIO
from unittest import mock
from zipfile import ZipFile, ZIP_DEFLATED

import api
from BaseTest import BaseTest


class LincomplianceMock:
    def __init__(self):
        self.upload_space = '.'
        self.workspace = '/root/project'

    def exec(self, filepath, name):
        return []


@mock.patch.object(api.package.resources, 'Lincompliance', return_value=LincomplianceMock())
class PackageTest(BaseTest):
    def test_post(self, *_) -> None:
        with BytesIO() as in_memory_zip:
            with ZipFile(in_memory_zip, 'w', ZIP_DEFLATED) as zf:
                zf.writestr("test.txt", b"Hello World !")
                zf.writestr("test2.txt", b"Bonjour le monde !")

            response = self.app.post('/package',
                                     data={'file': (in_memory_zip, "test.zip")},
                                     content_type='multipart/form-data')
            assert response.status_code == 201

        with BytesIO() as in_memory_zip:
            with ZipFile(in_memory_zip, 'w', ZIP_DEFLATED) as zf:
                zf.writestr("test.txt", b"Hello World !")
                zf.writestr("test2.txt", b"Bonjour le monde !")

            response = self.app.post('/package',
                                     data={'file': (in_memory_zip, 'test')},
                                     content_type='multipart/form-data')
            assert response.status_code == 415
            assert (loads(response.get_data(as_text=True)) == "Unsupported extension file for test")

        response = self.app.post('/package')
        assert response.status_code == 400
