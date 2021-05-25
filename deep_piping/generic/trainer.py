class GenericTrainer:
    def __init__(self, dataset, label, logger):
        self.dataset = dataset
        self.label = label
        self.logger = logger
        self.splitter = splitter
        self.resampler = resampler

    def fit(model):
        context = dict(logger=self.logger)

        without_label = set(self.dataset.columns) - { self.label }
        for train_index, test_index in self.splitter.split(
            self.dataset[without_label], self.dataset[self.label]):

            train_data = self.dataset.iloc[train_index]
            test_data = self.dataset.iloc[test_index]

            train_data = self.resampler.fit_resample(train_data[without_label],
                train_data[label])

            test_data = self.resampler.fit_resample(test_data[without_label],
                test_data[label])

            model.train(train_data, context)
            model.test(test_data, context)
