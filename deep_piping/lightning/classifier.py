#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import pytorch_lightning as plt
import torch


class LitFlexibleClassifier(plt.LightningModule):
    def __init__(self, dl_model, loaders, train_config, val_test_config,
        optimizer, batch_elements, extra_steps=[], lr_scheduler=None, **kwargs):

        super().__init__(**kwargs)

        self.dl_model = dl_model
        self.loaders = loaders
        self.train_config = train_config
        self.val_test_config = val_test_config
        self.optimizer = optimizer
        self.batch_elements = batch_elements
        self.extra_steps = extra_steps
        self.lr_scheduler = lr_scheduler

    def configure_optimizers(self):
        res = { 'optimizer': self.optimizer() }
        if self.lr_scheduler is not None:
            res['lr_scheduler'] = lr_scheduler()
        return res

    def training_step(self, batch, batch_idx):
        context = { k: batch[i] for i, k in enumerate(self.batch_elements) }
        feed = { k: context[v] for k, v in self.train_config['map_batch'].items() }
        output = self.dl_model(**feed)
        output = { k: output[i] for i, k in enumerate(self.train_config['output_elements']) }
        context.update(output)
        # print('context:', context)
        loss = self.train_config['loss'](context)
        self.log_dict({ 'loss': loss }, on_step=True)
        output['loss'] = loss
        if 'y_true' in context:
            output['y_true'] = context['y_true']
        return output

    def training_step_end(self, batch_parts):
        # print('batch_parts:', batch_parts)
        batch_parts = dict(batch_parts)
        batch_parts['loss'] = batch_parts['loss'].mean()
        return batch_parts

    def training_epoch_end(self, outputs):
        context = { k: [ out[k] for out in outputs ] for k in outputs[0].keys() }
        context = { k: torch.cat(v, dim=0) if k != 'loss' else sum(v)/len(v) for k, v in context.items() }
        context['phase'] = 'train'
        context['logger'] = self.logger
        context['loop_index'] = self.current_epoch
        for st in self.extra_steps:
            st(context)

    def validation_step(self, batch, batch_idx):
        context = { k: batch[i] for i, k in enumerate(self.batch_elements) }
        feed = { k: context[v] for k, v in self.val_test_config['map_batch'].items() }
        output = self.dl_model(**feed)
        output = { k: output[i] for i, k in enumerate(self.val_test_config['output_elements']) }
        context.update(output)
        if 'loss' in self.val_test_config:
            loss = self.val_test_config['loss'](context)
            self.log_dict({ 'val_loss': loss })
            output['val_loss'] = loss
        if 'y_true' in context:
            output['y_true'] = context['y_true']
        return output

    def validation_step_end(self, batch_parts):
        batch_parts = dict(batch_parts)
        batch_parts['val_loss'] = batch_parts['val_loss'].mean()
        return batch_parts

    def validation_epoch_end(self, outputs):
        context = { k: [ out[k] for out in outputs ] for k in outputs[0].keys() }
        context = { k: torch.cat(v, dim=0) if k != 'val_loss' else sum(v)/len(v) for k, v in context.items() }
        context['phase'] = 'val'
        context['logger'] = self.logger
        context['loop_index'] = self.current_epoch
        for st in self.extra_steps:
            st(context)

    def test_step(self, batch, batch_idx):
        context = { k: batch[i] for i, k in enumerate(self.batch_elements) }
        feed = { k: context[v] for k, v in self.val_test_config['map_batch'].items() }
        output = self.dl_model(**feed)
        output = { k: output[i] for i, k in enumerate(self.val_test_config['output_elements']) }
        context.update(output)
        if 'loss' in self.val_test_config:
            loss = self.val_test_config['loss'](context)
            self.log_dict({ 'test_loss': loss })
            output['test_loss'] = loss
        if 'y_true' in context:
            output['y_true'] = context['y_true']
        return output

    def test_step_end(self, batch_parts):
        batch_parts = dict(batch_parts)
        batch_parts['test_loss'] = batch_parts['test_loss'].mean()
        return batch_parts

    def test_epoch_end(self, outputs):
        context = { k: [ out[k] for out in outputs ] for k in outputs[0].keys() }
        context = { k: torch.cat(v, dim=0) if k != 'test_loss' else sum(v)/len(v) for k, v in context.items() }
        context['phase'] = 'test'
        context['logger'] = self.logger
        context['loop_index'] = self.current_epoch
        for st in self.extra_steps:
            st(context)

    def train_dataloader(self):
        return self.loaders.train_dataloader()

    def val_dataloader(self):
        return self.loaders.val_dataloader()

    def test_dataloader(self):
        return self.loaders.test_dataloader()
