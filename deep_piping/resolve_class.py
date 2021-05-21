import importlib


def resolve_class(class_name):
    if hasattr(__builtins__, class_name):
        return getattr(__builtins__, class_name)
    class_name = class_name.split('.')
    module_name, class_name = '.'.join(class_name[:-1]), class_name[-1]
    mod = importlib.import_module(module_name)
    cls = getattr(mod, class_name)
    return cls
