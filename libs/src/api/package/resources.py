#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import getenv
from os.path import join

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask import abort

from process import Lincompliance
from api.logger import getLogger
from common.file import extract_name, mkdir_if_not_exist
from common.strings import has_ext
from dao.package import PackageDAO


def _save_tmpfile(file: FileStorage, filepath: str) -> None:
    try:
        file.save(filepath)
    except IOError as e:
        abort(507, f"Could not upload the file: {e}")


def _post_parser() -> reqparse.RequestParser:
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file',
                        type=FileStorage, help="File is needed to upload",
                        location='files', required=True)
    return parser


class Packages(Resource):
    ALLOWED_EXTENSION = ["zip"]
    UPLOAD_SPACE = getenv("LIN_TMPDIR", "/tmp/linapi")

    def __init__(self):
        self.lincompliance = Lincompliance()
        self.dao = PackageDAO(self.lincompliance.workspace)
        self._logger = getLogger(__name__)

        mkdir_if_not_exist(self.UPLOAD_SPACE)
        self.post_parser = _post_parser()

    def _post_parse(self) -> (FileStorage, str):
        args = self.post_parser.parse_args()

        if not has_ext(args['file'].filename, self.ALLOWED_EXTENSION):
            self._logger(f"Unsupported extension file for {args['file'].filename}")
            abort(415, f"Unsupported extension file for {args['file'].filename}")
        return args['file'], join(self.UPLOAD_SPACE, secure_filename(args['file'].filename))

    def post(self):
        file, filepath = self._post_parse()
        name: str = extract_name(filepath)
        data: list = self.dao.get_package(name)

        if data is not None:
            self._logger.debug(f"{name}: Package data recovered - End of request.")
            return data, 200
        self._logger.debug(f"{name}: No package with this name found. Process launched.")
        _save_tmpfile(file, filepath)
        try:
            data = self.lincompliance.exec_zip(filepath, name)
        except Exception as e:
            raise abort(422, e)
        self._logger.debug(f"{name}: End of process.")
        self.dao.save_package(name, data)
        self._logger.debug(f"{name}: Package data saved.")
        return data, 201
