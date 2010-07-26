from django import http
from django.utils.http import urlencode


class TransformError(Exception):
    pass

def reverse_resolver(url, *args, **kwargs):
    """Treats given url as url-pattern name and tries to revese it"""
    from django.core.urlresolvers import reverse, NoReverseMatch

    try:
        return reverse(url, args=args, kwargs=kwargs)
    except NoReverseMatch:
        pass

    return None  # FIXME: maybe raise Exception

def format_resolver(url, *args, **kwargs):
    """Processes given url as string with python format syntax"""
    try:
        return url % args
    except TypeError:
        try:
            return url % kwargs
        except KeyError:
            pass
        return None  # FIXME: maybe raise Exception

def transform_to(request, url, params=None, to_url=None, to_query=None, process=None,
                 rewrites=None, defaults=None, as_kwargs=False, resolver=None):
    """Generates url with given template and params."""
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

    # Rewrite arguments
    for key, new_name in rewrites.iteritems():
        try:
            params[new_name] = params.pop(key)
        except KeyError:
            pass

    # Advanced arguments processing
    for keys, func in process.iteritems():
        if not isinstance(keys, (list, tuple)):
            keys = [keys]

        try:
            res = func(request, *[params[key] for key in keys])
            if isinstance(res, dict):
                params.update(res)
            elif len(keys) == 1:
                params[keys[0]] = res
        except KeyError:
            pass

    # Passing **kwargs or *args to resolver
    try:
        if as_kwargs:
            args = ()
            kwargs = dict([(key, params[key])
                               for key in to_url
                                   if key in params])
        else:
            args = [params[key]
                    for key in to_url
                        if key in params]
            kwargs = {}
    except KeyError, e:
        raise TransformError(e)

    # In hard cases we can set 'url' and 'params' programmatically
    if callable(url):
        url = url(request, params)
        if isinstance(url, http.HttpResponse):
            return url

    url = resolver(url, *args, **kwargs)

    if not url:
        raise TransformError("Can't resolve url: '%s', with args: %s, %s." %
                             (url, args, kwargs))

    params = dict([(key, not isinstance(value, list) and [value] or value)
                for key, value in params.iteritems()])

    query = urlencode(
        [(key, value)
                for key in to_query
                    for value in params.get(key, [])]
    )

    if query:
        query = '?' + query

    return url + query
