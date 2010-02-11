from django import http
from django.utils.http import urlencode

from legacy import transform_to

def redirect_to(request, url, to_url=None, to_query=None, process=None,
                rewrites=None, defaults=None, as_kwargs=False, resolver=None,
                *view_args, **view_kwargs):
    data = request.GET.copy()
    data.update(views_kwargs)

    try:
        new_url = transform_to(
            url, data, to_url, to_query, process, rewrites, defaults, as_kwargs, resolver
        )
    except Exception:
        raise http.Http404("Cannot transform url")

    return http.HttpResponsePermanentRedirect(new_url)
