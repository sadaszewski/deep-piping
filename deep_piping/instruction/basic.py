import sklearn.metrics


class Instruction:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Fit(Instruction):
    def __call__(self, context):
        context['ml_model'].fit(context['x'])


class Predict(Instruction):
    def __call__(self, context):
        y_pred = context['ml_model'].predict(context['x'])
        context['y_pred'] = y_pred


class ComputeScores(Instruction):
    def __init__(self, scores):
        self.scores = scores

    def __call__(self, context):
        y_pred = context['y_pred']
        y_true = context['y_true']
        res = {}
        for snam in self.scores:
            s = getattr(sklearn.metrics, snam + '_score')
            res[snam] = s(y_true, y_pred)
        context['scores'] = res


class LogScores(Instruction):
    def __call__(self):
        for snam, sval in context['scores'].items():
            context['logger'].log_metric(snam, sval)
