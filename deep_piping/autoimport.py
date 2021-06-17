#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import ast
import importlib
import types


def autoimport(expr, names):
    # names = list(names)
    try:
        t = ast.parse(expr)
    except SyntaxError:
        raise SyntaxError('Syntax error in expression: %s' % expr)
    res = {}
    assert len(t.body) == 1
    for n in ast.walk(t):
        n.is_parent = False
    for n in ast.walk(t):
        for ch in ast.iter_child_nodes(n):
            ch.parent = n
            n.is_parent = True
    for n in ast.walk(t):
        if not isinstance(n, ast.Name):
            continue
        if n.id in names and not isinstance(names[n.id], types.ModuleType):
            continue
        path = [ n.id ]
        mod = None
        while True:
            try:
                # print('Trying to load:', '.'.join(path), '...')
                mod = importlib.import_module('.'.join(path))
                if isinstance(n, ast.Name):
                    res[n.id] = mod
                    #names.append(n.id)
            except ModuleNotFoundError:
                # print('Failed')
                break
            if not isinstance(n.parent, ast.Attribute):
                break
            n = n.parent
            path.append(n.attr)
    return res, t
