import importlib
from .create_object import create_object


def materialize_config(config, args, debug=False):
    container = { 'args': args }
    if 'import' in config:
        for k, v in config['import'].items():
            container[k] = importlib.import_module(v)

    for k, v in config.items():
        if debug:
            print('Processing:', k, '...')
        container[k] = create_object(v, container)

    return container
