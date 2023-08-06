import numpy as np
from sets.core import Embedding


class OneHot(Embedding):

    def __init__(self, words, embed_data=False, embed_target=False):
        table = self._construct_table(words)
        super().__init__(table, len(table), embed_data, embed_target)

    @staticmethod
    def _construct_table(words):
        table = {}
        words = set(words)
        for word in words:
            vector = np.zeros(len(words))
            vector[len(table)] = 1
            table[word] = vector
        return table
