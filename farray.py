import pickle
import os
from os import path
from glob import glob

def load(path):
    '''Load an object from file'''
    with open(path, 'rb') as file:
        return pickle.load(file)

def dump(object, path):
    '''Save the object to file'''
    with open(path, 'wb') as file:
        return pickle.dump(object, file)

class mrecord():
    '''A simple in-memory (key, value) record'''

    def __init__(self, key, value):
        self.key = key
        self.value = value

class frecord():
    '''A simple on-disk (key, value) record'''

    def __init__(self, key, value, prefix):
        self.key_f = prefix + '-key.pickle'
        self.value_f = prefix + '-value.pickle'
        self.key = key
        self.value = value

    @property
    def key(self):
        return load(self.key_f)

    @key.setter
    def key(self, key):
        dump(key, self.key_f)

    @property
    def value(self):
        return load(self.value_f)

    @value.setter
    def value(self, value):
        dump(value, self.value_f)

    def clear(self):
        os.remove(self.key_f)
        os.remove(self.value_f)

class marray():
    '''A simple in-memory array of records'''

    def __init__(self):
        self.array = []

    def insert(self, i, key, value):
        self.array.insert(i, mrecord(key, value))

    def __getitem__(self, i):
        return self.array[i]

    def __len__(self):
        return len(self.array)

    def __delitem__(self, i):
        del self.array[i]

    def clear(self):
        del self.array[:]

class farray(marray):
    '''A simple on-disk array of records'''

    def __init__(self, datadir, array_f):
        super().__init__()
        self.datadir = datadir
        self.array_f = array_f
        self.id = 0
        if not path.exists(datadir):
            os.makedirs(datadir)

    def insert(self, i, key, value):
        prefix = path.join(self.datadir, str(self.id))
        self.array.insert(i, frecord(key, value, prefix))
        self.id = self.id + 1
        dump(self, self.array_f)

    def __delitem__(self, i):
        self[i].clear()
        super().__delitem__(i)
        dump(self, self.array_f)

    def clear(self):
        for r in self:
            r.clear()
        super().clear()
        os.remove(self.array_f)

def newarray(datadir = None, clear = False):
    '''Make a simple array of records that can be stored in memory or on disk, or load one from disk'''
    if clear and path.isdir(datadir):
        for file in glob(path.join(datadir, '*.pickle')):
            os.remove(file)
    if datadir:
        array_f = path.join(datadir, 'array.pickle')
        if path.isfile(array_f):
            return load(array_f)
        else:
            return farray(datadir, array_f)
    else:
        return marray()
