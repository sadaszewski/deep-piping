#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

class GenericModel:
    def __init__(self, ml_model, train_steps, test_steps, label):
        self.ml_model = ml_model()
        self.train_steps = train_steps
        self.test_steps = test_steps
        self.label = label

    def train(self, train_data, context):
        context = dict(context)
        context.update(dict(ml_model=self.ml_model,
            data=train_data, phase='train',
            y_true=train_data[self.label]))
        for st in self.train_steps:
            st(context)
        return context

    def test(self, test_data, context):
        context = dict(context)
        context.update(dict(ml_model=self.ml_model,
            data=test_data, phase='test',
            y_true=test_data[self.label]))
        for st in self.test_steps:
            st(context)
        return context
