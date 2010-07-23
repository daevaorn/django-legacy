from django import http
from django.utils.http import urlencode

from legacy import transform_to, TransformError

def redirect_to(request, url, to_url=None, to_query=None, process=None,
                rewrites=None, defaults=None, as_kwargs=False, resolver=None,
                *view_args, **view_kwargs):
    data = request.GET.copy()
    data.update(view_kwargs)

    try:
        response = transform_to(
            request, url, data, to_url, to_query, process, rewrites, defaults, as_kwargs, resolver
        )
    except TransformError, e:
        raise http.Http404("Cannot transform url: %s" % e)

    if isinstance(response, http.HttpResponse):
        return response

    return http.HttpResponsePermanentRedirect(response)
