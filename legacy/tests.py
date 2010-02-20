from legacy import *

__test__ = {'': r"""
    Simple transform
    >>> transform_to(
    ...    '/event/%s/', {'a': 1}, to_url=['a'],
    ...    resolver=format_resolver
    ... )
    '/event/1/'

    Transform with custom processing
    >>> transform_to(
    ...    '/event/%s/', {'a': 1, 'b': 2},
    ...    to_url=['ab'], process={('a', 'b'): lambda a, b: {'ab': '%s%s' % (a, b)}},
    ...    resolver=format_resolver
    ... )
    '/event/12/'

    Transforn with processing and rewrite
    >>> transform_to(
    ...    '/event/%s/%s/', {'a': 1, 'b': 2},
    ...    to_url=['a', 'c'], process={'c': lambda c: c + 1},rewrites={'b': 'c'},
    ...    resolver=format_resolver
    ... )
    '/event/1/3/'

    Transforn with list in params
    >>> transform_to(
    ...    '/event/%s/', {'a': 1, 'b': [2, 3]},
    ...    to_url=['a'], to_query=['b'],
    ...    resolver=format_resolver
    ... )
    '/event/1/?b=2&b=3'
"""
}
