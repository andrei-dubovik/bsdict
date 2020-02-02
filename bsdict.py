from bslt import *
from farray import *

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

