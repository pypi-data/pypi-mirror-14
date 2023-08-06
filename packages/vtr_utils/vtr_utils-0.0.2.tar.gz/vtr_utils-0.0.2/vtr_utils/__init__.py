import collections

def dict_update(d, u):
    """Recursive dict update

    :param d: goal dict
    :param u: updates for d
    :return: new dict
    """
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = dict_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d