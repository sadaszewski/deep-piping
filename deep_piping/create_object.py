#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import ruamel.yaml as yaml
from .autoimport import autoimport
from .resolve_class import resolve_class
import importlib
import ast


class Factory:
    def __init__(self, cls, args, kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.cls(*self.args, **self.kwargs)


def is_identifier(s):
    t = ast.parse(s)
    if isinstance(t, ast.Module) and len(t.body) == 1 and \
        isinstance(t.body[0], ast.Expr) and isinstance(t.body[0].value, ast.Name):
        return True
    return False
    
    
class CreateObjects:
    def __init__(self, config, args, verbose):
        self.config = config
        self.args = args
        self.verbose = verbose
        
        self.top_level_objects_in_creation = set()
        self.top_level_objects_created = set()
        
    def execute(self):
        config = self.config
        args = self.args
        verbose = self.verbose
        
        container = { 'args': args }
        if 'import' in config:
            for k, v in config['import'].items():
                container[k] = importlib.import_module(v)

        for k, v in config.items():
            if verbose:
                print('Processing:', k, '...')
            if k in self.top_level_objects_created:
                if verbose:
                    print(f'Skipping {k} - already pulled in by a dependency...')
                continue
            container[k] = self.create_top_level_object(k, v, container)

        return container
    
    def create_top_level_object(self, name, objdef, container):
        if name in self.top_level_objects_created:
            raise RuntimeError(f'This top-level object ({name}) has already been created - this should never happen.')
        if name in self.top_level_objects_in_creation:
            raise RuntimeError(f'Circular dependency detected ({name})')
        self.top_level_objects_in_creation.add(name)
        res = self.create_object(objdef, container)
        self.top_level_objects_in_creation.remove(name)
        self.top_level_objects_created.add(name)
        return res

    def create_object(self, objdef, container):
        if isinstance(objdef, list):
            return [ self.create_object(item, container) for item in objdef ]
        elif type(objdef) in [ yaml.scalarstring.SingleQuotedScalarString,
            yaml.scalarstring.DoubleQuotedScalarString,
            yaml.scalarstring.LiteralScalarString,
            yaml.scalarstring.FoldedScalarString ]:
            return str(objdef)
        elif type(objdef) == str:
            names = dir(__builtins__) + list(globals().keys()) + list(container.keys())
            if is_identifier(objdef) and objdef not in names and objdef in self.config.keys():
                if self.verbose:
                    print(f'Unknown identifier {objdef}, trying to create dependency from config...')
                container[objdef] = self.create_top_level_object(objdef, self.config[objdef], container)
                names.append(objdef)
            imp, _ = autoimport(objdef, names)
            container.update(imp)
            return eval(objdef, globals(), container)
        elif isinstance(objdef, dict) and 'class' in objdef and \
            type([ k for k in objdef.keys() if k == 'class' ][0]) == str:
            cls = self.create_object(objdef['class'], container)
            args = {}
            kwargs = self.create_object(objdef.get('kwargs', {}), container)
            for k, v in objdef.items():
                if k in [ 'class', '__factory__', 'kwargs' ]:
                    continue
                if type(k) == int:
                    args[k] = self.create_object(v, container)
                else:
                    kwargs[k] = self.create_object(v, container)
            args = [ args[i] for i in range(len(args)) ]
            if '__factory__' in objdef and objdef['__factory__']:
                return Factory(cls, args, kwargs)
            return cls(*args, **kwargs)
        elif isinstance(objdef, dict):
            return { k: self.create_object(v, container) \
                for k, v in objdef.items() }
        else:
            return objdef
