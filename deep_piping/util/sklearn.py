class SklearnWrapper:
    def __init__(self, sk_model, label):
        self.sk_model = sk_model()
        self.label = label

    def fit(self, data):
        without_label = [ nam for nam in data.columns if nam != self.label ]
        self.sk_model.fit(data[without_label], data[self.label])

    def predict(self, data):
        without_label = [ nam for nam in data.columns if nam != self.label ]
        return self.sk_model.predict(data[without_label])

    def predict_proba(self, data):
        without_label = [ nam for nam in data.columns if nam != self.label ]
        return self.sk_model.predict_proba(data[without_label])
