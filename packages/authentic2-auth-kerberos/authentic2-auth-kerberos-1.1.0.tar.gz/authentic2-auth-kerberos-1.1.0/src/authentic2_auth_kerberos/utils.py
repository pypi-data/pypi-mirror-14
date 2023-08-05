import urlparse
import urllib

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def redirect_next(request, url, **kwargs):
    '''Redirect to URL, add or replace parameters with kwargs

       You can use relative or fully qualifier, or view names. You can provide
       view args and kwargs using named argument args and kwargs.
    '''
    # specialize on the next url parameter as it is so frequent
    if 'next' in request.REQUEST:
        next_url = request.REQUEST.get('next')
        kwargs['next'] = next_url
    if not url.startswith('/') and not url.startswith('http:') and not url.startswith('https:'):
        view_args = kwargs.pop('args', None)
        view_kwargs = kwargs.pop('kwargs', None)
        url = reverse(url, args=view_args, kwargs=view_kwargs)
    parsed = urlparse.urlparse(url)
    params = urlparse.parse_qs(parsed.query)
    for key in kwargs.keys():
        if kwargs[key] is None:
            del kwargs[key]
    params.update(kwargs)
    url = urlparse.urlunparse(parsed[:4] + (urllib.urlencode(params),) + parsed[5:])
    return HttpResponseRedirect(url)
