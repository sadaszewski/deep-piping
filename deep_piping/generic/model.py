class GenericModel:
    def __init__(self, ml_model, train_steps, test_steps, label):
        self.ml_model = ml_model
        self.train_steps = train_steps
        self.test_steps = test_steps
        self.label = label

    def train(train_data, context):
        context = dict(context)
        context.update(dict(data=train_data, y_true=train_data[self.label]))
        for st in self.train_steps:
            st(context)
        return context

    def test(test_data, context):
        context = dict(context)
        context.update(dict(data=test_data, y_true=test_data[self.label]))
        for st in self.train_steps:
            st(context)
        return context
