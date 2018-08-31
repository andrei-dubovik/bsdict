import unittest
import importlib
import fplt
from fplt import *
import numpy as np

# Force reloading (needed during the development cycle)
importlib.reload(fplt)

def gt(x, y):
    '''Test whether x > y'''
    return lt(y, x)

def eq(x, y):
    '''Test whether x == y'''
    return not (lt(x, y) or gt(x, y))

class Galaxy():
    pass

class TestsLibrary(unittest.TestCase):

    def lt_test(self, x, y):
        '''Test under the assumption that x < y'''
        self.assertTrue(lt(x, y))
        self.assertFalse(lt(y, x))
        self.assertFalse(lt(x, x))
        self.assertFalse(lt(y, y))

    def eq_test(self, x, y):
        '''Test under the assumption that x == y'''
        self.assertTrue(eq(x, y))

class BuiltinTests(TestsLibrary):

    def test_sametype(self):
        self.lt_test(False, True)
        self.lt_test(1, 2)
        self.lt_test(1.0, 2.0)
        self.lt_test(1+2J, 2+0.5J)
        self.lt_test(1+1J, 1+2J)
        self.lt_test("de", "abc")
        self.lt_test("ab", "ac")
        self.lt_test(b"de", b"abc")
        self.lt_test(b"ab", b"ac")
        self.lt_test(np.nan, -1.0)

    def test_sametype_containers(self):
        self.lt_test([4,5], [1,2,3])
        self.lt_test([1,2], [2,1])
        self.lt_test([1,2], [1,3])
        self.lt_test({'c': 3}, {'a': 1, 'b': 2})
        self.lt_test((4,5), (1,2,3))
        self.lt_test((1,2), (2,1))
        self.lt_test((1,2), (1,3))
        self.lt_test({'a': 2}, {'b': 1})
        self.lt_test({'a': 1}, {'a': 2})
        self.lt_test(set([3,4]), set([1,2,3]))
        self.lt_test(set([2,1]), set([1,3]))
        self.lt_test(set([2,2]), set([1,2]))
        self.lt_test(frozenset([3,4]), frozenset([1,2,3]))
        self.lt_test(frozenset([2,1]), frozenset([1,3]))
        self.lt_test(frozenset([2,2]), frozenset([1,2]))

    def test_crosstype(self):
        self.lt_test(None, False)
        self.lt_test(1, "ab")
        self.lt_test(set([1]), {'a': 1})

    def test_upcasting(self):
        self.eq_test(0, False)
        self.eq_test(1, True)
        self.eq_test(1, 1.0 + 0.0J)
        self.eq_test("a", b"a")
        self.eq_test([1,2], (1,2))
        self.eq_test(set([1,2]), frozenset([1,2]))

    def test_sameness(self):
        e = abs_tol/2
        self.eq_test(1, 1-e)
        self.eq_test(1, 1+e*1J)
        self.eq_test([1,2,3], [1-e,2+e,3])

    def test_unsupported(self):
        with self.assertRaises(RuntimeError):
            lt(Galaxy(), Galaxy())

class NumpyTests(TestsLibrary):

    def lt_test(self, x, y):
        '''Convert arguments to numpy arrays and apply tests'''
        with np.errstate(all = 'raise'):
            super().lt_test(np.array(x), np.array(y))

    def eq_test(self, x, y):
        '''Convert arguments to numpy arrays and apply tests'''
        with np.errstate(all = 'raise'):
            super().eq_test(np.array(x), np.array(y))

    def test_sametype(self):
        self.lt_test([1,2,3], [1,3,0])
        self.lt_test([1,np.nan], [1,-1])
        self.lt_test([1,np.nan], [1,-np.inf])
        self.lt_test([1,np.nan,2], [1,np.nan,np.inf])
        self.lt_test([1+1J, 2+2J], [1+1J, 3+1J])
        self.lt_test([1+2J, 2+2J], [1+1J, 3+1J])
        self.lt_test([1+1J, 2+2J], [1+1J, 2+3J])

    def test_shapes(self):
        self.lt_test([2,3], [1,2,0])
        self.lt_test([[1,2,3],[4,5,6]], [[1,2],[2,3],[4,5]])
        self.lt_test([[1,2,3],[4,5,6]], [[1,2,3],[4,7,7]])

    def test_crosstype(self):
        self.lt_test([1,2], [1.0,2.1])
        self.lt_test([1,2], [1.0+0.1J,2.0])

    def test_upcasting(self):
        self.eq_test([1,2,3], [1.0,2.0,3.0])
        self.eq_test([1,2], [1+0J,2+0J])
        self.eq_test([1.0], [1-0J])

    def test_sameness(self):
        e = abs_tol/2
        self.eq_test([1+1J,-2,np.nan], [1+(1-e)*1J,-2+e-e*1J,np.nan])

# Run unit tests
unittest.main(verbosity = 2, exit = False)
