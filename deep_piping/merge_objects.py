class DeleteMe:
    pass


def merge_objects(a, b):
    if type(a) == dict:
        if type(a) != type(b):
            raise TypeError
        if '__delete__' in b and b['__delete__']:
            return DeleteMe
        if '__replace__' in b and b['__replace__']:
            return dict(b)
        a = dict(a)
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
