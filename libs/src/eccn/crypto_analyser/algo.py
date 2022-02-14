#!/usr/bin/env python3
from os import popen

from api.logger import getLogger


class Algo:
    def __init__(self, algos, strong_algos, exclude_word, extensions) -> None:
        self.ALGORITHMS = algos.replace("\n", "").split(',')
        self.STRONG_ALGORITHMS = strong_algos.replace("\n", "").split(',')
        self.EXCLUDE_WORDS = "|".join(exclude_word.replace("\n", "").split(','))
        self.EXTENSIONS_INCLUSION = " --include *.".join(['', *(extensions.split(','))])

        self.found_algo = []
        self._logger = getLogger(__name__)

    def grep(self, filepath, keyword, exclude_words):
        # ce n'est pas l'idéal, mais on filtre, quel que soit l'algo par rapport à des mots clés estimés inutiles.
        # si ce mode est trouvé dans la chaîne on ignore le résultat.
        # Cela évite ainsi beaucoup de faux positifs avec un léger risque de faux négatifs
        color = 'always' if exclude_words != '' else 'never'
        grep_command = f'grep --color={color} -irnE {self.EXTENSIONS_INCLUSION} "{keyword}" {filepath}'
        if exclude_words != '':
            grep_command += f'| grep -Evi "{exclude_words}"'
        self._logger.debug(f'Grep command to execute: {grep_command}')
        return popen(grep_command)

    def grep_helper(self, filepath, keywords, exclude_words=''):
        return self.grep(filepath, keywords, exclude_words).read()

    # 4. lancer un grep avec des mots clés (pour crypto simple et crypto forte)
    # recherche insensible à la casse et sous chaîne
    def grep_crypto(self, filepath):
        try:
            return self.grep_helper(filepath, "crypt|cipher")
        except NameError:
            self._logger.error("error subprocess call")

    # 9.chercher les algorithms forts utilisés
    def grep_strong_algo(self) -> bool:
        result = any(elem in self.STRONG_ALGORITHMS for elem in self.found_algo)
        # Clearing list
        self.found_algo.clear()
        return bool(result)

    # 7. retourner le resultat trouvé pour les algorithms utilisés
    def grep_algos_strict(self, filepath):
        result = self.grep_helper(filepath, "|".join(self.ALGORITHMS), self.EXCLUDE_WORDS)
        return [result] if result != '' else []

    # 6. chercher les algorithmes utilisés
    # TODO on pourrait améliorer en utilisant l'output de result_algo
    def grep_algo(self, filepath):
        algos = []
        result_grep = self.grep_helper(filepath, "|".join(self.ALGORITHMS), self.EXCLUDE_WORDS)
        for algo in self.ALGORITHMS:
            if algo.lower() in result_grep.lower():
                algos.append(algo)
                self.found_algo.append(algo)
        return "/".join(algos) if len(algos) > 1 else "".join(algos)
