
from api.logger import getLogger
from requests import get


class PrologInterface:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self._logger = getLogger('Prolog')
        self.available = False
        try:
            get(self.server_ip)
            self.available = True
        except Exception as e:
            self._logger.critical(f'Prolog server not available {e}')

    def get(self, license: str, score: int) -> str:
        try:
            return get(f'{self.server_ip}/eccn', params={'license': license, 'score': score}).text
        except Exception as e:
            return 'Not found'
