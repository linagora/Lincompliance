#!/usr/bin/env python3

from .algo import Algo
from api.logger import getLogger, LOG_PATH


def extract_filepath(name):
    return '/'.join(['unknown' if not d else d for d in name.split(":")])


class CryptoAnalyser:
    CRYPTO_KEYWORD_WEIGHT = 1
    ALGO_WEIGHT = 5

    def __init__(self, conf):
        self.algofuncs = Algo(conf['AllEncryption']['algorithms'],
                              conf['StrongEncryption']['algorithms_strong'],
                              conf['AllEncryption']['exclude_words'],
                              conf['ExtensionsTargets'])

        self._logger = getLogger(__name__)

    def exec(self, name: str, version: int, filepath: str) -> dict:
        self._logger.debug(f'{name}-{version}: Filepath given to test: {filepath}.')
        crypto = self.algofuncs.grep_crypto(filepath)
        score: int = crypto.count("\n") * self.CRYPTO_KEYWORD_WEIGHT
        self._logger.debug(f'{name}-{version}: grep crypto result with a score of {score} is: \n{crypto}')
        # recherche de la liste d'algos
        algoList = self.algofuncs.grep_algo(filepath)
        self._logger.debug(f'{name}-{version}: algorithms found {algoList}')

        # une liste qu'on va séparer avec des retours charriot
        algo_result = "\n".join(self.algofuncs.grep_algos_strict(filepath))
        score = score + algo_result.count("\n") * self.ALGO_WEIGHT
        self._logger.debug(f'{name}-{version}: grep strict algo result change score to {score} and is\n{algo_result}')


        # vérification s'il y a des algo forts d'encryptage
        # TODO pourquoi chercher dans le source, on peut très bien chercher
        # dans algoList ? Ce n'est qu'une optimisation
        ifStrongEncryption = self.algofuncs.grep_strong_algo()

        if crypto == '' and algo_result == '':
            self._logger.critical(f'{name}-{version}: Dependency not downloaded')

        with open(f'{LOG_PATH}/reports/{name}{version}.log', 'w') as reportf:
            # si on a trouvé des algos de crypto, on force la crypto à vrai
            reportf.write(str(crypto).strip('[]').replace(" ", "_"))
            reportf.write(str(algo_result).strip('[]').replace(" ", "_"))
        return {
            'score': score,
            'ifCrypto': bool(algoList or ifStrongEncryption or crypto),
            'algoList': algoList,
            'ifStrongEncryption': ifStrongEncryption
        }

