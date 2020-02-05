import unittest
import random
import importlib
import bsdict
# Force reloading (needed during the development cycle)
importlib.reload(bsdict)
from bsdict import bsdict, memoizer

CHOICES = [
    lambda: random.randint(2,10),
    lambda: random.random() + random.random()*1J,
    lambda: ''.join(chr(i) for i in random.sample(range(97, 123), random.randint(1,10))),
    lambda: [random_key() for i in range(random.randint(1, 4))],
]

def random_key():
    return random.choice(CHOICES)()

class TestsLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_size = 1000
        cls.seed = 4454887
        cls.del_chance = 4
        cls.d = bsdict()

    def test_comprehensive(self):
        random.seed(self.seed)
        test_dict = bsdict()
        keys = []
        for i in range(self.test_size):
            key = random_key()
            keys.append(key)
            test_dict.setdefault(key, set()).add(i)
            if random.randrange(self.del_chance) == 0:
                key = random.choice(keys)
                if key:
                    for j in test_dict[key]:
                        keys[j] = None
                    del test_dict[key]

        for i, key in enumerate(keys):
            if key:
                test_dict[key].remove(i)

        for key in keys:
            if key:
                self.assertTrue(len(test_dict[key]) == 0)

        for key in keys:
            if key and key in test_dict:
                del test_dict[key]

        self.assertTrue(len(test_dict) == 0)

    def test_01_setitem(self):
        self.d['a'] = 1
        self.d[[1,2]] = 2
        v = self.d.setdefault({1:1, 2:2}, 3)
        self.assertEqual(v, 3)

    def test_02_len(self):
        self.assertEqual(len(self.d), 3)

    def test_03_contains(self):
        self.assertTrue([1,2] in self.d)
        self.assertFalse([1,3] in self.d)

    def test_04_getitem(self):
        self.assertEqual(self.d[[1,2]], 2)
        with self.assertRaises(KeyError):
            self.d[[1,3]]
        self.assertEqual(self.d.get('b', -1), -1)

    def test_05_delitem(self):
        with self.assertRaises(KeyError):
            del self.d['b']
        del self.d[[1,2]]
        self.assertFalse([1,2] in self.d)

    def test_06_iterators(self):
        self.assertEqual(list(self.d), ['a', {1:1, 2:2}])
        self.assertEqual(list(self.d.keys()), ['a', {1:1, 2:2}])
        self.assertEqual(list(reversed(self.d)), [{1:1, 2:2}, 'a'])
        self.assertEqual(list(self.d.values()), [1, 3])
        self.assertEqual(list(self.d.items()), [('a', 1), ({1:1, 2:2}, 3)])

    def test_07_repr(self):
        self.assertEqual(repr(self.d), "{'a': 1, {1: 1, 2: 2}: 3}")

    def test_08_pop(self):
        with self.assertRaises(KeyError):
            self.d.pop('b')
        self.assertEqual(self.d.pop({1:1, 2:2}), 3)
        self.assertEqual(self.d.popitem(), ('a', 1))
        with self.assertRaises(KeyError):
            self.d.popitem()

    def test_clear(self):
        self.d['a'] = 1
        self.d['b'] = 2
        self.d.clear()
        self.assertEqual(len(self.d), 0)

    def test_memoization(self):
        counter = 0
        cached = memoizer()

        @cached
        def mysum(x, y):
            nonlocal counter
            counter += 1
            return x + y

        @cached
        def myprod(x, y):
            nonlocal counter
            counter += 1
            return x*y

        for i in range(2):
            mysum(1, 2)
            mysum(1, 3)
            myprod(1, 2)

        self.assertEqual(counter, 3)


# Run unit tests
unittest.main(verbosity = 2, exit = False)
