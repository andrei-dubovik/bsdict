from functools import singledispatch
import math
import operator

# Define numerical tolerance when testing for equality
# (Relative tolerance is disabled on purpose because it is inconsistent with
# lexicographical ordering)
abs_tol = 1e-6
default_enc = 'utf-8'

# Supported types:
# none, bool, int, float, complex,
# str, bytes, bytearray,
# list, tuple, dict, set, frozenset

# Define upcasting rules
upcast_tree = {complex: 2, float: 2*3, int: 2*3*5, bool: 2*3*5*7,
               list: 11, tuple: 11*13,
               bytearray: 17, bytes: 17*19, str: 17*19*23,
               set: 29, frozenset: 29*31}
upcast_func = {b:a for a,b in upcast_tree.items()}
upcast_func[1] = lambda x: fqtn(x)
upcast_func[17] = lambda x: bytearray(x.encode(default_enc) if type(x) == str else x)
upcast_func[17*19] = lambda x: bytes(x.encode(default_enc) if type(x) == str else x)

def fqtn(x):
    '''Get the fully qualified name of type of x'''
    if x == None:
        return ''
    t = type(x)
    return t.__module__ + '.' + t.__name__

def upcast(x, y):
    '''Upcast numerical arguments to the least general common type'''
    p = math.gcd(*(upcast_tree.get(type(v), 1) for v in (x, y)))
    return tuple(upcast_func[p](v) for v in (x, y))

def lt(x, y):
    '''Test whether x < y'''
    return _lt(x, y) if type(x) == type(y) else _lt(*upcast(x, y))

@singledispatch
def _lt(x, y):
    '''Test whether x < y when both have the same type'''
    if x == None:
        return False
    raise RuntimeError("Type '{}' is not ordered".format(fqtn(x)))

# Define comparion operators for built-in numeric types
@_lt.register(bool)
def _(x, y):
    return x < y

@_lt.register(int)
def _(x, y):
    return x < y

@_lt.register(float)
def _(x, y):
    return x + abs_tol < y

@_lt.register(complex)
def _(x, y):
    return _lt(x.real, y.real) or (not _lt(y.real, x.real) and _lt(x.imag, y.imag))

# Define comparion operators for built-in string and bytes types
def lex_len(x, y, lt = operator.lt):
    '''x < y if len(x) < len(y) or len(x) == len(y) and x < y'''
    lx, ly = len(x), len(y)
    return lx < ly or (lx == ly and lt(x, y))

@_lt.register(str)
def _(x, y):
    return lex_len(x, y)

@_lt.register(bytes)
def _(x, y):
    return lex_len(x, y)

@_lt.register(bytearray)
def _(x, y):
    return lex_len(x, y)

# Define comparison operators for built-in containers
def lex_iter(iterator):
    '''Lexicographical comparator'''
    for x, y in iterator:
        if lt(x, y): return True
        if lt(y, x): return False
    return False

@_lt.register(list)
def _(x, y):
    return lex_len(x, y, lt = lambda x, y: lex_iter(zip(x, y)))

@_lt.register(tuple)
def _(x, y):
    return _lt(list(x), list(y))

@_lt.register(dict)
def _(x, y):
    return _lt(sorted(x.items()), sorted(y.items()))

@_lt.register(set)
def _(x, y):
    return _lt(sorted(x), sorted(y))

@_lt.register(frozenset)
def _(x, y):
    return _lt(set(x), set(y))
