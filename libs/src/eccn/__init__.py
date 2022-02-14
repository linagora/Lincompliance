#!/usr/bin/env python3

from logging import getLogger

from common.file import extract_json
from api.logger import getLogger
from .crypto_analyser import CryptoAnalyser
from .interface import PrologInterface


def extract_filepath(name):
    return '/'.join(['unknown' if not d else d for d in name.split(":")])


class ECCN:
    def __init__(self, prolog_ip: str, crypto_conf: str):
        self._logger = getLogger('eccn')
        self._prolog_interface = PrologInterface(prolog_ip)
        self.crypto_analyser = CryptoAnalyser(extract_json(crypto_conf))

    def exec(self, data: dict, source: str) -> list:
        self._logger.info(f"Execution launched with {len(data['analyzer']['result']['packages'])} elements.")
        result = []
        for package in data["analyzer"]["result"]["packages"]:
            result.append(self.analyse(package, source))
        return result

    def analyse(self, package: dict, source: str) -> dict:
        package_id = package["package"]["id"]
        name = package_id.split(':')[2]
        version = package_id.split(':')[3]

        self._logger.info(f'Analysis of package {name}:{version}.')

        crypto = self.crypto_analyser.exec(name, version, f'{source}/{extract_filepath(package_id)}')
        code = self._prolog_interface.get(package["package"]["declared_licenses_processed"].get('spdx_expression', 'unknown'),
                                          crypto['score'])

        return {
            'name': name,
            'version': version,
            'url': package["package"]["homepage_url"],
            'description': package["package"]["description"].replace(",", ""),
            'licence': "|".join(package["package"]["declared_licenses"]),
            'code': code,
            **crypto
        }
