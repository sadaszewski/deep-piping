import sklearn.metrics
import numpy as np


class Instruction:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Fit(Instruction):
    def __init__(self, fit_kwargs):
        self.fit_kwargs = fit_kwargs

    def __call__(self, context):
        context['ml_model'].fit(context['data'], **self.fit_kwargs)


class Predict(Instruction):
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
    def __init__(self, scores):
        self.scores = scores

    def __call__(self, context):
        y_true = context['data'][context['label']]
        res = {}
        for snam in self.scores:
            s = getattr(sklearn.metrics, snam + '_score')
            if snam in [ 'roc_auc' ]:
                res[snam] = s(y_true, context['y_score'])
            else:
                res[snam] = s(y_true, context['y_pred'])
        context['scores'] = res


class LogScores(Instruction):
    def __call__(self, context):
        metrics = { context['phase'] + '_' + k: v \
            for k, v in context['scores'].items() }
        context['logger'].log_metrics(metrics,
            step=context['loop_index'])
