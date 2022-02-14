#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import CalledProcessError, run

from api.logger import getLogger


class Ort:
    def __init__(self, ort_path: str):
        self.ort_path = ort_path
        self._logger = getLogger(__name__)

    def assembler(self, command: str, input_file: str, output_file: str, fmt: str) -> list:
        cmd = [self.ort_path,
               "--info",
               command,
               "-i", input_file,
               "-o", output_file]
        cmd[3:3] = [] if not fmt else ["-f", fmt]
        return cmd

    def exec_cmd(self, cmd: str, inputs: str, outputs: str, fmt: str = ""):
        self._logger.info(f"Launch {cmd}")
        try:
            with open('/var/log/linapi/ort.log', 'a') as f:
                run(self.assembler(cmd,
                                   inputs,
                                   outputs,
                                   fmt), stdout=f, stderr=f)
        except CalledProcessError as e:
            self._logger.error(f'\n{e}')
