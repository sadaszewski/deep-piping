#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import pytorch_lightning as plt


class LitFlexibleModel(plt.LightningModule):
    def __init__(self, dl_model, loaders, train_ins, val_ins, test_ins, optimizer, lr_scheduler=None, **kwargs):
        super().__init__(**kwargs)

        self.dl_model = dl_model
        self.loaders = loaders
        self.instructions = dict(train=train_ins,
            val=val_ins, test=test_ins)
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def step_template(self, phase, batch, batch_idx):
        context = dict(phase=phase, callback='step',
            batch=batch, batch_idx=batch_idx, model=self,
            ml_model=self.dl_model, result={})
        for insn in self.instructions[phase]:
            if 'step' not in insn.callback_mask:
                continue
            insn(context)
        if 'result' in context:
            return context['result']
        return {}

    def step_end_template(self, phase, batch_parts):
        context = dict(phase=phase, callback='step_end',
            batch_parts=batch_parts, model=self,
            ml_model=self.dl_model, result={})
        for insn in self.instructions[phase]:
            if 'step_end' not in insn.callback_mask:
                continue
            insn(context)
        if 'result' in context:
            return context['result']
        return {}

    def epoch_end_template(self, phase, outputs):
        context = dict(phase=phase, callback='epoch_end',
            outputs=outputs, model=self,
            ml_model=self.dl_model, result={})
        for insn in self.instructions[phase]:
            if 'epoch_end' not in insn.callback_mask:
                continue
            insn(context)
        if 'result' in context:
            return context['result']
        return {}

    def configure_optimizers(self):
        res = { 'optimizer': self.optimizer() }
        if self.lr_scheduler is not None:
            res['lr_scheduler'] = lr_scheduler()
        return res

    def training_step(self, batch, batch_idx):
        return self.step_template('train', batch, batch_idx)

    def training_step_end(self, batch_parts):
        return self.step_end_template('train', batch_parts)

    def training_epoch_end(self, outputs):
        return self.epoch_end_template('train', outputs)

    def validation_step(self, batch, batch_idx):
        return self.step_template('val', batch, batch_idx)

    def validation_step_end(self, batch_parts):
        return self.step_end_template('val', batch_parts)

    def validation_epoch_end(self, outputs):
        return self.epoch_end_template('val', outputs)

    def test_step(self, batch, batch_idx):
        return self.step_template('test', batch, batch_idx)

    def test_step_end(self, batch_parts):
        return self.step_end_template('test', batch_parts)

    def test_epoch_end(self, outputs):
        return self.epoch_end_template('test', outputs)

    def train_dataloader(self):
        return self.loaders.train_dataloader()

    def val_dataloader(self):
        return self.loaders.val_dataloader()

    def test_dataloader(self):
        return self.loaders.test_dataloader()
