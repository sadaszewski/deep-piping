import ruamel.yaml as yaml
from .autoimport import autoimport
from .resolve_class import resolve_class


def create_object(objdef, container):
    if type(objdef) == list:
        return [ create_object(item, container) for item in objdef ]
    elif type(objdef) in [ yaml.scalarstring.SingleQuotedScalarString,
        yaml.scalarstring.DoubleQuotedScalarString,
        yaml.scalarstring.LiteralScalarString,
        yaml.scalarstring.FoldedScalarString ]:
        return str(objdef)
    elif type(objdef) == str:
        names = dir(__builtins__) + list(globals().keys()) + list(container.keys())
        imp, _ = autoimport(objdef, names)
        container.update(imp)
        return eval(objdef, globals(), container)
    elif type(objdef) == dict and 'class' in objdef and \
        type([ k for k in objdef.keys() if k == 'class' ][0]) == str:
        cls = resolve_class(objdef['class'])
        args = {}
        kwargs = {}
        for k, v in objdef.items():
            if k == 'class':
                continue
            if type(k) == int:
                args[k] = create_object(v, container)
            else:
                kwargs[k] = create_object(v, container)
        args = [ args[i] for i in range(len(args)) ]
        return cls(*args, **kwargs)
    elif type(objdef) == dict:
        return { k: create_object(v, container) \
            for k, v in objdef.items() }
    else:
        return objdef
