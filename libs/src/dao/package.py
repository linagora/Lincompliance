# TODO: create link to db instead of this temporary file system
from csv import DictWriter, DictReader
from os.path import isfile, join
from typing import Optional

from api.logger import getLogger


class PackageDAO:
    FIELDNAMES = ['name', 'version', 'url', 'description', 'ifCrypto', 'algoList', 'ifStrongEncryption', 'score',
                       'licence', 'code']

    def __init__(self, location):
        self.location = location
        self._logger = getLogger('Package DAO')

    def get_filename(self, name: str) -> str:
        return join(self.location, f'{name}-results.csv')

    def get_package(self, name: str) -> Optional[list]:
        filename = self.get_filename(name)
        data = []

        if not isfile(filename):
            return None
        with open(filename, 'r') as f:
            self._logger.debug(f'File succesfully opened, data ready to be read.')
            data.extend(DictReader(f, fieldnames=self.FIELDNAMES))
        return data

    def save_package(self, name: str, data: list) -> None:
        with open(self.get_filename(name), 'w') as f:
            self._logger.debug(f'File succesfully opened, data ready to be write.')
            w = DictWriter(f, fieldnames=self.FIELDNAMES)
            w.writerows(data)
        self._logger.debug(f'Data for project {name} saved.')
