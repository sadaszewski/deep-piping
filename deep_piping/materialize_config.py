#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import importlib
from .create_object import CreateObjects


def materialize_config(config, args, verbose=False, overrides={}):
    create_objects = CreateObjects(config, args, verbose)
    container = create_objects.execute()
    
    for k, v in overrides.items():
        if verbose:
            print('Overriding:', k, '...')
        if callable(v):
            container[k] = v(container)
        else:
            container[k] = v

    return container
