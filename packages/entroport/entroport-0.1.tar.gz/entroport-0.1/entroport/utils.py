from __future__ import division, absolute_import
import statsmodels.api as sm
import numpy as np
from itertools import chain

def arrmap(f, seq):
    """Applies a function returning a n-tuple of arrays to seq and collapses the
    resulting list of tuples of tuples of arrays to a list of n arrays 

    >>> import numpy as np
    >>> np.random.seed(123)
    >>> map(lambda x: (np.random.randint(0, 10, size=3),
    ... np.random.randint(0, 10, size=4)), range(4)) #doctest: +NORMALIZE_WHITESPACE
    [(array([2, 2, 6]), array([1, 3, 9, 6])),
     (array([1, 0, 1]), array([9, 0, 0, 9])),
     (array([3, 4, 0]), array([0, 4, 1, 7])),
     (array([3, 2, 4]), array([7, 2, 4, 8]))]
    >>> np.random.seed(123)
    >>> arrmap(lambda x: (np.random.randint(0, 10, size=3),
    ... np.random.randint(0, 10, size=4)), range(4)) #doctest: +NORMALIZE_WHITESPACE
    [array([2, 2, 6, 1, 0, 1, 3, 4, 0, 3, 2, 4]),
     array([1, 3, 9, 6, 9, 0, 0, 9, 0, 4, 1, 7, 7, 2, 4, 8])]
    """
    nestedlist = zip(*map(f, seq))
    return map(lambda x:
               np.array(list(chain(*nestedlist[x]))),
               range(len(nestedlist)))

def window(seq, size, step=1):
    """Yields the moving window of size `size` with step size `step`
    over the sequence `seq`

    >>> seq = list(range(10))
    >>> list(window(seq, 5, 2))
    [[0, 1, 2, 3, 4], [2, 3, 4, 5, 6], [4, 5, 6, 7, 8]]
    """

    nchuncks = (len(seq) - size) // step + 1
    for i in range(0, nchuncks * step, step):
        yield seq[i:i+size]

