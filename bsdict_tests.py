import unittest
import random
import importlib
import bsdict
# Force reloading (needed during the development cycle)
importlib.reload(bsdict)
from bsdict import bsdict

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

# Run unit tests
unittest.main(verbosity = 2, exit = False)
