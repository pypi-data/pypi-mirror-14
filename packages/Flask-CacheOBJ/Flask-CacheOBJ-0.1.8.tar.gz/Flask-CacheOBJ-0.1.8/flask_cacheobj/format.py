# -*- coding: utf-8 -*-

import re
from inspect import getargspec

# pylint: disable=C0103
old_pattern = re.compile(r'%\w')
new_pattern = re.compile(r'\{(\w+(\.\w+|\[\w+\])?)\}')
__formaters = {}

def _formater(text):
    def translator(k):
        if '.' in k:
            name,attr = k.split('.')
            if name.isdigit():
                k = int(name)
                return lambda *a, **kw: getattr(a[k], attr)
            return lambda *a, **kw: getattr(kw[name], attr)
        else:
            if k.isdigit():
                return lambda *a, **kw: a[int(k)]
            return lambda *a, **kw: kw[k]
    args = [translator(k) for k, _ in new_pattern.findall(text)]
    if args:
        if old_pattern.findall(text):
            raise Exception('mixed format is not allowed')
        f = new_pattern.sub('%s', text)
        return lambda *a, **kw: f % tuple([k(*a,**kw) for k in args])
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        n = len(old_pattern.findall(text))
        return lambda *a, **kw: text % tuple(a[:n])

def format_key_pattern(text, *a, **kw):
    """Format template with arguments.

    >>> format_key_pattern('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    >>> format_key_pattern('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    >>> format_key_pattern('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    >>> class Obj: id = 3
    >>> format_key_pattern('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    """
    f = __formaters.get(text)
    if f is None:
        f = _formater(text)
        __formaters[text] = f
    return f(*a, **kw)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
