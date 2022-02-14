#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : __init__.py
# License           : AGPL-3.0-or-later
# Author            : Pierre Marty <pmarty@linagora.com>
# Date              : 2022.01.19
# Last Modified Date: 2022.01.19
# Last Modified By  : Pierre Marty <pmarty@linagora.com>

from os import path, getenv

from api.logger import getLogger
from common.file import mkdir_if_not_exist, extract_json, clean, unzip_remove
from eccn import ECCN
from process.ort import Ort


class Lincompliance:
    FORMAT = "json"
    ANALYSER_SUFFIX = "analyser"
    ANALYSER_RESULT = f'analyser-result{FORMAT}'
    DOWNLOADER_SUFFIX = 'sources'

    ORT_PATH = getenv('ORT_PATH', '/usr/local/bin/ort')
    PROLOG_URL = getenv('PROLOG_URL', 'http://172.20.0.5')

    def __init__(self,
                 root: str = "/root",
                 workspace: str = "project",):
        self._logger = getLogger(__name__)
        workspace = getenv('LIN_WORKSPACE', path.join(root, workspace))
        self._logger.debug(f'Workspace: {workspace}')
        self.workspace = workspace
        self.ort = Ort(self.ORT_PATH)
        self.eccn = ECCN(self.PROLOG_URL, path.join(getenv('LIN_CONFDIR'), 'crypto_analyser.json'))

        mkdir_if_not_exist(self.workspace)
        self._logger.debug('Main lincompliance class created.')

    def exec(self, src: str, name: str) -> list:
        analyser_result_folder = path.join(self.workspace, f'{name}-{self.ANALYSER_SUFFIX}')
        analyser_result = f'{analyser_result_folder}/analyzer-result.{self.FORMAT}'
        downloader_result = path.join(self.workspace, f'{name}-{self.DOWNLOADER_SUFFIX}')

        try:
            self.ort.exec_cmd('analyze', src, analyser_result_folder, self.FORMAT)
            self._logger.debug('Analyse done')
            self.ort.exec_cmd('download', analyser_result, downloader_result)
            self._logger.debug('Start ECCN execution.')
            data = self.eccn.exec(extract_json(analyser_result), downloader_result)
        finally:
            self._logger.debug(f"Folders cleans: {src}, {analyser_result_folder}, {downloader_result}")
            clean(src, analyser_result_folder, downloader_result)
        return data

    def exec_zip(self, filepath: str, name: str) -> list:
        src = path.join(self.workspace, name)
        unzip_remove(filepath, src)
        self._logger.debug(f'{name}: Sources saved to {src}')
        return self.exec(src, name)
