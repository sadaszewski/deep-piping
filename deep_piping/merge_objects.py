#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

class DeleteMe:
    pass


def merge_objects(a, b):
    if isinstance(a, dict):
        if not isinstance(a, type(b)) and not isinstance(b, type(a)): # type(a) != type(b):
            raise TypeError('%s != %s' % ( type(a), type(b) ))

        if '__delete__' in b and b['__delete__']:
            return DeleteMe

        if '__replace__' in b and b['__replace__']:
            b = b.__class__(b)
            del b['__replace__']
            return b

        a = a.__class__(a)

        for k, v in b.items():
            tmp = merge_objects(a[k], b[k]) \
                if k in a else b[k]
            if tmp == DeleteMe:
                del a[k]
            else:
                a[k] = tmp
        return a
    #elif type(a) == list:
    #    if type(a) != type(b):
    #        raise ValueError
    #    return a + b
    else:
        return b
