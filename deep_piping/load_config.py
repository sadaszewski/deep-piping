import os
import ruamel.yaml as yaml
from .merge_objects import merge_objects


def load_config(fname):
    path, _ = os.path.split(os.path.abspath(fname))
    with open(fname, 'r') as f:
        config = yaml.round_trip_load(f, preserve_quotes=True)
    # config['path'] = os.path.abspath(fname)

    if 'base' in config:
        res = {}
        base = config['base']
        if not isinstance(base, list):
            base = [ base ]
        for b in base:
            base_config = load_config(os.path.join(path, b))
            res = merge_objects(res, base_config)
        res = merge_objects(res, config)
    else:
        res = config

    return res
