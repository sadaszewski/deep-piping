#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import importlib
from .create_object import create_object


def materialize_config(config, args, verbose=False, overrides={}):
    container = { 'args': args }
    if 'import' in config:
        for k, v in config['import'].items():
            container[k] = importlib.import_module(v)

    for k, v in config.items():
        if verbose:
            print('Processing:', k, '...')
        if k in overrides:
            container[k] = overrides[k](container)
        else:
            container[k] = create_object(v, container)

    return container
