import unittest
from btree import *

def gt(x, y):
    '''Test whether x > y'''
    return lt(y, x)

def eq(x, y):
    '''Test whether x == y'''
    return not (lt(x, y) or gt(x, y))

class ComparisonTests(unittest.TestCase):

    def lt_test(self, x, y):
        '''Test under the assumption that x < y'''
        self.assertTrue(lt(x, y))
        self.assertFalse(lt(y, x))
        self.assertFalse(lt(x, x))
        self.assertFalse(lt(y, y))

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
        self.assertTrue(eq(0, False))
        self.assertTrue(eq(1, True))
        self.assertTrue(eq(1, 1.0 + 0.0J))
        self.assertTrue(eq("a", b"a"))
        self.assertTrue(eq([1,2], (1,2)))
        self.assertTrue(eq(set([1,2]), frozenset([1,2])))

    def test_sameness(self):
        e = abs_tol/2
        self.assertTrue(eq(1, 1-e))
        self.assertTrue(eq(1, 1+e*1J))
        self.assertTrue(eq([1,2,3], [1-e,2+e,3]))

# unittest.main(verbosity = 2, exit = False)
