import nltk
import numpy as np
from sets.core import Step, Dataset


class Tokenize(Step):

    def __call__(self, dataset):
        # pylint: disable=arguments-differ
        data = self._tokenize(dataset.data)
        data = self._pad(data)
        return Dataset(data, dataset.target)

    @staticmethod
    def _tokenize(data):
        return [nltk.word_tokenize(x) for x in data]

    @staticmethod
    def _pad(data):
        width = max(len(x) for x in data)
        for index, tokens in enumerate(data):
            missing = width - len(tokens)
            data[index] += ['' for _ in range(missing)]
        return np.array(data)
