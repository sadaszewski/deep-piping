#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

class GenericTrainer:
    def __init__(self, dataset, label, logger, splitter, resampler=None, n_classes=None):
        self.dataset = dataset
        self.label = label
        self.logger = logger
        self.splitter = splitter
        self.resampler = resampler
        self.n_classes = n_classes

    def fit(self, model_factory):
        label = self.label
        without_label = [ nam for nam in self.dataset.columns if nam != label ]
        for loop_index, (train_index, test_index) in enumerate(self.splitter.split(
            self.dataset[without_label], self.dataset[label])):

            model = model_factory()

            context = dict(logger=self.logger, loop_index=loop_index,
                label=self.label, n_classes=self.n_classes)

            train_data = self.dataset.iloc[train_index]
            test_data = self.dataset.iloc[test_index]

            if self.resampler is not None:
                train_data = self.resampler.fit_resample(train_data)
                test_data = self.resampler.fit_resample(test_data)

            model.train(train_data, context)
            model.test(test_data, context)
