import unittest
import importlib
import farray
# Force reloading (needed during the development cycle)
importlib.reload(farray)
from farray import *
import shutil
import os
import sys

class TestsLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.datadir = 'cache'

    def lifecycle_test(self, a):
        a.insert(0, 'k1', 'v1')
        a.insert(1, 'k2', 'v2')
        a.insert(2, 'k3', 'v3')
        del a[1]
        m = [(r.key, r.value) for r in a]
        self.assertEqual(m, [('k1', 'v1'), ('k3', 'v3')])

    def test_memory(self):
        self.lifecycle_test(newarray())

    def test_disk(self):
        self.lifecycle_test(newarray(datadir = self.datadir, clear = True))

    def test_persistence(self):
        a = newarray(datadir = self.datadir, clear = True)
        a.insert(0, 'k1', 'v1')
        a.insert(1, 'k2', 'v2')
        del a
        a = newarray(datadir = self.datadir)
        m = [(r.key, r.value) for r in a]
        self.assertEqual(m, [('k1', 'v1'), ('k2', 'v2')])

    def test_clear(self):
        a = newarray(datadir = self.datadir, clear = True)
        self.lifecycle_test(a)
        a.clear()
        self.assertTrue(len(os.listdir(self.datadir)) == 0)

    def test_refcounts(self):
        a1 = newarray()
        a1.insert(0, 6494286202494917, 'v')
        a2 = newarray(datadir = self.datadir, clear = True)
        a2.insert(0, 2774367369060229, 'v')
        k1 = a1[0].key
        k2 = a2[0].key
        self.assertTrue(sys.getrefcount(k1), 4) # test_refcounts, record, k1, getrefcount
        self.assertTrue(sys.getrefcount(k2), 2) # k2, getrefcount

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.datadir)

# Run unit tests
unittest.main(verbosity = 2, exit = False)
