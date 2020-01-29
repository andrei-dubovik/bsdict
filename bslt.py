from functools import singledispatch
import operator
import numpy as np

# Define global constants
default_enc = 'utf-8'

# Supported types:
# none,
# bool, int, float (incl. nan), complex,
# str, bytes, bytearray,
# list, tuple, dict, set, frozenset,
# numpy.ndarray (bool, int, float, complex).

# Prepare numpy.ndarray subtype wrappers
class ndarray_int(np.ndarray):
    pass

class ndarray_float(np.ndarray):
    pass

class ndarray_complex(np.ndarray):
    pass

# Define upcasting rules
def encode_rules(tree, func):
    '''Encode a hierarchy with the only branch point at the root'''
    func = {(i,j):func.get(n, n) for i,l in enumerate(tree) for j,n in enumerate(l)}
    tree = {n:(i,j) for i,l in enumerate(tree) for j,n in enumerate(l)}
    return tree, func

def lcp(x, y):
    '''Least common parent'''
    return (x[0], min(x[1], y[1])) if x[0] == y[0] else (0,0)

upcast_tree = ([
    [0],
    [complex, float, int, bool],
    [list, tuple],
    [bytearray, bytes, str],
    [set, frozenset],
    [ndarray_complex, ndarray_float, ndarray_int],
])

upcast_func = {
    0: lambda x: fqtn(x),
    bytearray: lambda x: bytearray(x.encode(default_enc) if type(x) == str else x),
    bytes: lambda x: bytes(x.encode(default_enc) if type(x) == str else x),
    ndarray_complex: lambda x: x.view(ndarray_complex),
    ndarray_float: lambda x: x.view(ndarray_float),
    ndarray_int: lambda x: x.view(ndarray_int),
}

upcast_tree, upcast_func = encode_rules(upcast_tree, upcast_func)

def fqtn(x):
    '''Get the fully qualified name of type of x'''
    t = type(x)
    if t.__name__ == 'NoneType':
        return ''
    if t == np.ndarray:
        return x.dtype.name + '.' + t.__name__ + '.' + t.__module__
    return t.__name__ + '.' + t.__module__

def upcast(x, y):
    '''Upcast arguments to the least general common type'''
    p = lcp(*(upcast_tree.get(type(v), (0,0)) for v in (x, y)))
    return tuple(upcast_func[p](v) for v in (x, y))

def downcast_ndarray(x):
    '''Wrap ndarray subtypes into own classes'''
    if type(x) == np.ndarray:
        if x.dtype.kind in ['b', 'i', 'u']:
            return x.view(ndarray_int)
        if x.dtype.kind == 'f':
            return x.view(ndarray_float)
        if x.dtype.kind == 'c':
            return x.view(ndarray_complex)
    return x

def lt(x, y):
    '''Test whether x < y'''
    x, y = downcast_ndarray(x), downcast_ndarray(y)
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
    return not np.isnan(y) and (np.isnan(x) or x < y)

@_lt.register(complex)
def _(x, y):
    xr, xi, yr, yi = x.real, x.imag, y.real, y.imag
    return _lt(xr, yr) or (not _lt(yr, xr) and _lt(xi, yi))

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

# Numpy ndarray
def compare_shapes(func):
    '''A wrapper around func(x,y) that first compares shapes of x and y'''
    def wrapper(x, y):
        xs, ys = x.shape, y.shape
        if _lt(xs, ys):
            return True
        if _lt(ys, xs):
            return False
        return func(x, y)
    return wrapper

@_lt.register(ndarray_int)
@compare_shapes
def _(x, y):
    diff = (x < y)[x != y]
    return diff[0] if len(diff) else False

@_lt.register(ndarray_float)
@compare_shapes
def _(x, y):
    xr, yr = np.nan_to_num(x), np.nan_to_num(y)
    xm, ym = np.isnan(x), np.isnan(y)
    xlty = ~ym & (xm | (xr < yr))
    yltx = ~xm & (ym | (yr < xr))
    diff = xlty[xlty | yltx]
    return diff[0] if len(diff) else False

@_lt.register(ndarray_complex)
def _(x, y):
    xr, xi = np.real(x).view(ndarray_float), np.imag(x).view(ndarray_float)
    yr, yi = np.real(y).view(ndarray_float), np.imag(y).view(ndarray_float)
    return _lt(xr, yr) or (not _lt(yr, xr) and _lt(xi, yi))
