#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import pandas as pd
import numpy as np


class ImblearnWrapper:
    def __init__(self, resampler, label):
        self.resampler = resampler
        self.label = label

    def fit_resample(self, data):
        resampler = self.resampler()
        label = self.label
        without_label = [ nam for nam in data.columns if nam != label ]
        X, y = resampler.fit_resample(data[without_label], data[label])
        res = pd.DataFrame(np.concatenate([ X, y.to_numpy().reshape((-1, 1)) ], axis=1),
            columns=without_label + [ label ])
        return res
