class GenericModel:
    def __init__(self, ml_model, train_steps, test_steps, label):
        self.ml_model = ml_model()
        self.train_steps = train_steps
        self.test_steps = test_steps
        self.label = label

    def train(self, train_data, context):
        context = dict(context)
        context.update(dict(ml_model=self.ml_model,
            data=train_data, phase='train'))
        for st in self.train_steps:
            st(context)
        return context

    def test(self, test_data, context):
        context = dict(context)
        context.update(dict(ml_model=self.ml_model,
            data=test_data, phase='test'))
        for st in self.test_steps:
            st(context)
        return context
