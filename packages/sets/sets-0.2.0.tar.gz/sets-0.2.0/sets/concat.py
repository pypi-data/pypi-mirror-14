import numpy as np
from sets.core import Step, Dataset


class Concat(Step):

    def __init__(self, targets_from=0):
        self._targets_from = targets_from

    def __call__(self, *datasets):
        data = np.concatenate([x.data for x in datasets], axis=2)
        target = datasets[self._targets_from].target
        return Dataset(data, target)
