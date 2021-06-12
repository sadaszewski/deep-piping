#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import os
import shutil


def remove_checkpoints(logger, args):
    ckpt_path = os.path.join(args.save_dir, logger.experiment_id, logger.run_id, 'checkpoints')
    shutil.rmtree(ckpt_path)


def log_hyperparams(logger, config, args):
    # logger.log_hyperparams({ 'config_path': config['path'] })
    logger.log_hyperparams({ k: str(v) for k, v in vars(args).items() })
    #for k, v in config.items():
    #    logger.log_hyperparams({ f'config.{k}': json.dumps(v) })
