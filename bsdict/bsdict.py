from functools import wraps
from .bslt import *
from .farray import *

# Define global constants
WARNING = 'Memoization: loading cached results for {}(...)'

class bsdict():
    def __init__(self, datadir = None, clear = False):
        self.array = newarray(datadir = datadir, clear = clear)

    def __len__(self):
        return len(self.array)

    def search(self, key, debug = False):
        if debug:
            pdb.set_trace()
        lb, rb = -1, len(self)
        while True:
            if lb + 1 == rb:
                return rb, False
            m = (lb + rb)//2
            if lt(self.array[m].key, key):
                lb = m
            elif lt(key, self.array[m].key):
                rb = m
            else:
                return m, True

    def __contains__(self, key):
        i, status = self.search(key)
        return status

    def __getitem__(self, key):
        i, status = self.search(key)
        if status:
            return self.array[i].value
        else:
            raise KeyError(key)

    def get(self, key, default = None):
        i, status = self.search(key)
        if status:
            return self.array[i].value
        else:
            return default

    def __setitem__(self, key, value):
        i, status = self.search(key)
        if status:
            self.array[i].value = value
        else:
            self.array.insert(i, key, value)

    def setdefault(self, key, default = None):
        i, status = self.search(key)
        if status:
            return self.array[i].value
        else:
            self.array.insert(i, key, default)
            return default

    def __delitem__(self, key):
        i, status = self.search(key)
        if status:
            del self.array[i]
        else:
            raise KeyError(key)

    def keys(self):
        for r in self.array:
            yield r.key

    def __reversed__(self):
        for r in reversed(self.array):
            yield r.key

    def values(self):
        for r in self.array:
            yield r.value

    def items(self):
        for r in self.array:
            yield (r.key, r.value)

    def __iter__(self):
        return self.keys();

    def __repr__(self):
        txt = ', '.join(repr(k) + ': ' + repr(v) for k, v in self.items())
        return '{' + txt + '}'

    def clear(self):
        self.array.clear()

    def pop(self, key):
        i, status = self.search(key)
        if status:
            v = self.array[i].value
            del self.array[i]
            return v
        else:
            raise KeyError(key)

    def popitem(self):
        if len(self) == 0:
            raise KeyError('popitem(): dictionary is empty')
        r = self.array[-1]
        k, v = r.key, r.value
        del self.array[-1]
        return k, v


def qualname(func):
    '''Get a qualified name of a function'''
    if func.__module__ == '__main__':
        return func.__name__
    else:
        return func.__module__ + '.' + func.__name__

def memoizer(datadir = None, verbose = False):
    '''A basic memoizer that uses bsdict for storage'''
    cache = bsdict(datadir = datadir)

    def decorator(func):
        sig = (func.__code__.co_code, func.__code__.co_consts)

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (sig, args, kwargs)
            try:
                value = cache[key]
                if verbose:
                    print(WARNING.format(qualname(func)))
                return value
            except KeyError:
                value = func(*args, **kwargs)
                cache[key] = value
                return value

        return wrapper

    return decorator
