import torch


class SplitDatasets(Datasets):
    def __init__(self, dataset, ratios=(.5, .25, .25), seed=0):
        super().__init__()

        self.dataset = dataset
        self.ratios = ratios
        self.seed = seed

        g = torch.Generator().manual_seed(seed)
        n = len(dataset)
        perm = torch.randperm(n, generator=g)
        ratios = torch.round(torch.tensor(ratios) * n).to(torch.long).tolist()
        ratios[-1] = n - sum(ratios[:-1])
        perm = torch.split(perm, ratios)[:3]
        self.perm = perm = [ p.tolist() for p in perm ]

        self.subsets = [
            torch.utils.data.Subset(dataset, p) \
                for p in perm
        ]


    def __getitem__(self, index):
        return self.subsets[index]

    def __len__(self):
        return len(self.subsets)


class DataLoaders:
    def __init__(self, datasets, batch_size=32):
        self.datasets = datasets
        self.batch_size = batch_size

        self.loaders = [
            torch.utils.data.DataLoader(sub,
                num_workers=1, batch_size=self.batch_size,
                drop_last=False, shuffle=(i == 0)) \
                    for i, sub in enumerate(datasets)
        ]

    def __len__(self):
        return len(self.loaders)

    def __getitem__(self, index):
        return self.loaders[index]

    def train_dataloader(self):
        return self.loaders[0]

    def val_dataloader(self):
        return self.loaders[1]

    def test_dataloader(self):
        return self.loaders[2]