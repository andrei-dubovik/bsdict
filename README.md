# About
BSDict is a dictionary for Python that supports the following objects as keys:

* None,
* bool, int, float (including math.nan), complex,
* str, bytes, bytearray,
* list, tuple, dict, set, frozenset,
* numpy.ndarray (bool, int, float, complex).

Internally, a total lexicographical order is defined over all supported objects. A sorted array is then used for storage, and binary search is used for element lookup.

BSDict can be initialized in-memory or on-disc (persistent storage). If BSDict is initialized on-disc, then keys and values are stored in memory only as long as the client application has any references to them. So, the dictionary can be larger than available RAM.

This packages has been originally written to help memoize functions that accept complex data structures, including floating-point data, as arguments. Such functions are common in data analysis.

# Basic Usage

In-memory dictionary:

```python
from bsdict import bsdict
import numpy as np
data = bsdict()
key = {'s1': np.array([1.0, 10.0, np.nan])}
data[key] = 5
data
```

On-disc dictionary:

```python
from bsdict import bsdict
data = bsdict(datadir = 'cache')
# ...
data.clear()
```

# Warning

This is the first official release. Bug reports are welcome. (There are extensive test suits in the package, however.)

# Technical Notes

A simpler way to support arbitrary keys would be to pickle them and store their binary representation in a dictionary. There are two minor issues with approach. Firstly, identical dictionaries and sets might be serialized differently depending on the order in which they were composed (So they need to be recursively sorted). Secondly, numerical algorithms than run on multiple processes or on multiple machines might break floating-point determinism. If it desirable to consider nearly identical numbers as the same number, then with binary search that would possible, while with serialization that won't work. Then again, lexicographical ordering of vectors in inconsistent with near-match lookups, meaning that it would work fine often but not always. If you need near-match lookups, let me know, I'll add them as an option then.
