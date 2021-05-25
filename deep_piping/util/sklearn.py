class SklearnWrapper:
    def __init__(self, sk_model, label):
        self.sk_model = sk_model
        self.label = label

    def fit(data):
        without_label = set(data.columns) - set([ self.label ])
        self.sk_model.fit(data[without_label], data[label])

    def predict(data):
        without_label = set(data.columns) - set([ self.label ])
        return self.sk_model.predict(data[without_label])
