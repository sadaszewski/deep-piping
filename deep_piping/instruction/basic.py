#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import sklearn.metrics
import numpy as np
from .insn import Instruction
import torch
import inspect


class Fit(Instruction):
    def __init__(self, fit_kwargs={}, **kwargs):
        super().__init__(**kwargs)
        self.fit_kwargs = fit_kwargs

    def __call__(self, context):
        context['ml_model'].fit(context['data'], **self.fit_kwargs)


class Predict(Instruction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, context):
        ml_model = context['ml_model']
        y_pred = ml_model.predict(context['data'])
        context['y_pred'] = y_pred
        if hasattr(ml_model, 'predict_proba'):
            y_score = ml_model.predict_proba(context['data'])
            # print('y_score:', y_score)
            if len(y_score.shape) == 2 and context['n_classes'] == 2:
                y_score = np.array(y_score)[:, 1]
            context['y_score'] = y_score


class ComputeScores(Instruction):
    def __init__(self, scores, average='binary', **kwargs):
        super().__init__(**kwargs)
        self.scores = scores
        self.average = average

    def __call__(self, context):
        y_true = context['y_true']
        if isinstance(y_true, torch.Tensor):
            y_true = y_true.cpu()
        res = {}
        for snam in self.scores:
            s = getattr(sklearn.metrics, snam + '_score')
            def try_s(a, b):
                try:
                    return s(a, b, average=self.average)
                except:
                    pass
                return s(a, b)
            #argspec = inspect.getfullargspec(s)
            #if 'average' in argspec[0] or argspec[2] is not None:
            #    feed = dict(average=self.average)
            if snam in [ 'roc_auc' ]:
                y_score = context['y_score']
                if isinstance(y_score, torch.Tensor):
                    y_score = y_score.cpu()
                res[snam] = try_s(y_true, y_score)
            else:
                y_pred = context['y_pred']
                if isinstance(y_pred, torch.Tensor):
                    y_pred = y_pred.cpu()
                res[snam] = try_s(y_true, y_pred)
        context['scores'] = res


class LogScores(Instruction):
    def __init__(self, log_to_stdout=False, **kwargs):
        super().__init__(**kwargs)
        self.log_to_stdout = log_to_stdout

    def __call__(self, context):
        metrics = { context['phase'] + '_' + k: v \
            for k, v in context['scores'].items() }
        context['logger'].log_metrics(metrics,
            step=context['loop_index'])
        if self.log_to_stdout:
            print(metrics)
