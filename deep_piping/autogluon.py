#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

class AutogluonWrapper:
    def __init__(self, ag_model):
        self.ag_model

    def fit(self, X, y):
        self.ag_model.fit(X)
