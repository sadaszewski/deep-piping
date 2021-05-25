import sklearn.metrics


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
        y_pred = context['ml_model'].predict(context['data'])
        context['y_pred'] = y_pred


class ComputeScores(Instruction):
    def __init__(self, scores):
        self.scores = scores

    def __call__(self, context):
        y_pred = context['y_pred']
        y_true = context['data'][context['label']]
        res = {}
        for snam in self.scores:
            s = getattr(sklearn.metrics, snam + '_score')
            res[snam] = s(y_true, y_pred)
        context['scores'] = res


class LogScores(Instruction):
    def __call__(self, context):
        metrics = { context['phase'] + '_' + k: v \
            for k, v in context['scores'].items() }
        context['logger'].log_metrics(metrics,
            step=context['loop_index'])
