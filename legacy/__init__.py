from django.utils.http import urlencode

def reverse_resolver(url, *args, **kwargs):
    """Treats given url as url-pattern name and tries to revese it"""
    from django.core.urlresolvers import reverse, NoReverseMatch

    try:
        return reverse(url, args=args, kwargs=kwargs)
    except NoReverseMatch:
        pass

    return None

def format_resolver(url, *args, **kwargs):
    """Processes given url as string with python format syntax"""
    try:
        return url % args
    except TypeError:
        try:
            return url % kwargs
        except KeyError:
            pass
        return None

def transform_to(url, params=None, to_url=None, to_query=None, process=None,
                 rewrites=None, defaults=None, as_kwargs=False, resolver=None):
    r"""
    Generates url with given template and params.

    Examples:

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
    """
    params = params or {}
    to_url = to_url or []
    to_query = to_query or []
    process = process or {}
    rewrites = rewrites or {}
    defaults = defaults or {}
    resolver = resolver or reverse_resolver

    for key, default in defaults.iteritems():
        if key not in params:
            params[key] = callable(default) and default(request) or default

    for key, new_name in rewrites.iteritems():
        try:
            params[new_name] = params.pop(key)
        except KeyError:
            pass

    for keys, func in process.iteritems():
        if not isinstance(keys, (list, tuple)):
            keys = [keys]

        try:
            res = func(*[params[key] for key in keys])
            if isinstance(res, dict):
                params.update(res)
            elif len(keys) == 1:
                params[keys[0]] = res
        except KeyError:
            pass

    try:
        if as_kwargs:
            args = ()
            kwargs = dict([(key, params[key]) for key in to_url])
        else:
            args = [params[key] for key in to_url]
            kwargs = {}
    except KeyError:
        raise

    url = resolver(url, *args, **kwargs)

    if not url:
        return

    query = urlencode(dict([(key, params[key]) for key in to_query if key in params]))
    if query:
        query = '?' + query

    return url + query
