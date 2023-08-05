from collections import namedtuple
from operator import add

from dask.utils import raises
from dask.core import (istask, get, get_dependencies, flatten, subs,
                       preorder_traversal, quote, list2, _deps)


def contains(a, b):
    """

    >>> contains({'x': 1, 'y': 2}, {'x': 1})
    True
    >>> contains({'x': 1, 'y': 2}, {'z': 3})
    False
    """
    return all(a.get(k) == v for k, v in b.items())

def inc(x):
    return x + 1

def add(x, y):
    return x + y


def test_istask():
    assert istask((inc, 1))
    assert not istask(1)
    assert not istask((1, 2))
    f = namedtuple('f', ['x', 'y'])
    assert not istask(f(sum, 2))


d = {':x': 1,
     ':y': (inc, ':x'),
     ':z': (add, ':x', ':y')}


def test_preorder_traversal():
    t = (add, 1, 2)
    assert list(preorder_traversal(t)) == [add, 1, 2]
    t = (add, (add, 1, 2), (add, 3, 4))
    assert list(preorder_traversal(t)) == [add, add, 1, 2, add, 3, 4]
    t = (add, (sum, [1, 2]), 3)
    assert list(preorder_traversal(t)) == [add, sum, list, 1, 2, 3]


def test_get():
    assert get(d, ':x') == 1
    assert get(d, ':y') == 2
    assert get(d, ':z') == 3
    assert get(d, 'pass-through') == 'pass-through'


def test_memoized_get():
    try:
        import toolz
    except ImportError:
        return
    cache = dict()
    getm = toolz.memoize(get, cache=cache, key=lambda args, kwargs: args[1:])

    result = getm(d, ':z', get=getm)
    assert result == 3

    assert contains(cache, {(':x',): 1,
                            (':y',): 2,
                            (':z',): 3})

def test_data_not_in_dict_is_ok():
    d = {'x': 1, 'y': (add, 'x', 10)}
    assert get(d, 'y') == 11


def test_get_with_list():
    d = {'x': 1, 'y': 2, 'z': (sum, ['x', 'y'])}

    assert get(d, ['x', 'y']) == [1, 2]
    assert get(d, 'z') == 3


def test_get_with_nested_list():
    d = {'x': 1, 'y': 2, 'z': (sum, ['x', 'y'])}

    assert get(d, [['x'], 'y']) == [[1], 2]
    assert get(d, 'z') == 3


def test_get_works_with_unhashables_in_values():
    f = lambda x, y: x + len(y)
    d = {'x': 1, 'y': (f, 'x', set([1]))}

    assert get(d, 'y') == 2


def test_get_laziness():
    def isconcrete(arg):
        return isinstance(arg, list)

    d = {'x': 1, 'y': 2, 'z': (isconcrete, ['x', 'y'])}

    assert get(d, ['x', 'y']) == [1, 2]
    assert get(d, 'z') == False


def test_get_dependencies_nested():
    dsk = {'x': 1, 'y': 2,
           'z': (add, (inc, [['x']]), 'y')}

    assert get_dependencies(dsk, 'z') == set(['x', 'y'])


def test_get_dependencies_empty():
    dsk = {'x': (inc,)}
    assert get_dependencies(dsk, 'x') == set()


def test_get_dependencies_list():
    dsk = {'x': 1, 'y': 2, 'z': ['x', [(inc, 'y')]]}
    assert get_dependencies(dsk, 'z') == set(['x', 'y'])


def test_nested_tasks():
    d = {'x': 1,
         'y': (inc, 'x'),
         'z': (add, (inc, 'x'), 'y')}

    assert get(d, 'z') == 4


def test_get_stack_limit():
    d = dict(('x%s' % (i+1), (inc, 'x%s' % i)) for i in range(10000))
    d['x0'] = 0
    assert get(d, 'x10000') == 10000
    # introduce cycle
    d['x5000'] = (inc, 'x5001')
    assert raises(RuntimeError, lambda: get(d, 'x10000'))
    assert get(d, 'x4999') == 4999


def test_flatten():
    assert list(flatten(())) == []
    assert list(flatten('foo')) == ['foo']


def test_subs():
    assert subs((sum, [1, 'x']), 'x', 2) == (sum, [1, 2])
    assert subs((sum, [1, ['x']]), 'x', 2) == (sum, [1, [2]])


def test_subs_with_unfriendly_eq():
    try:
        import numpy as np
    except:
        return
    else:
        task = (np.sum, np.array([1, 2]))
        assert (subs(task, (4, 5), 1) == task) is True

    class MyException(Exception):
        pass

    class F():
        def __eq__(self, other):
            raise MyException()

    task = F()
    assert subs(task, 1, 2) is task


def test_subs_with_surprisingly_friendly_eq():
    try:
        import pandas as pd
    except:
        return
    else:
        df = pd.DataFrame()
        assert subs(df, 'x', 1) is df


def test_quote():
    literals = [[1, 2, 3], (add, 1, 2),
                [1, [2, 3]], (add, 1, (add, 2, 3))]

    for l in literals:
        assert get({'x': quote(l)}, 'x') == l


def test__deps():
    dsk = {'x': 1, 'y': 2}

    assert _deps(dsk, ['x', 'y']) == ['x', 'y']
