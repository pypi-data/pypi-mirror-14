import contextlib

from django.http import QueryDict
from django.core.urlresolvers import set_urlconf, NoReverseMatch, resolve, \
    Resolver404
from django.utils.six.moves.urllib.parse import urlsplit

from .http import HttpResponseSwitchRedirect
from .views import redirect_
from .app_settings import app_settings

@contextlib.contextmanager
def set_urlconf_from_host(host):
    # Find best match, falling back to DEFAULT_SUBDOMAIN
    for subdomain in app_settings.SUBDOMAINS:
        match = subdomain['_regex'].match(host)
        if match:
            kwargs = match.groupdict()
            break
    else:
        kwargs = {}
        subdomain = get_subdomain(app_settings.DEFAULT_SUBDOMAIN)

    set_urlconf(subdomain['urlconf'])

    try:
        yield subdomain, kwargs
    finally:
        set_urlconf(None)

def get_subdomain(name):
    try:
        return {x['name']: x for x in app_settings.SUBDOMAINS}[name]
    except KeyError:
        raise NoReverseMatch("No subdomain called %s exists" % name)

def from_dotted_path(fullpath):
    """
    Returns the specified attribute of a module, specified by a string.

    ``from_dotted_path('a.b.c.d')`` is roughly equivalent to::

        from a.b.c import d

    except that ``d`` is returned and not entered into the current namespace.
    """

    module, attr = fullpath.rsplit('.', 1)

    return getattr(
        __import__(module, {}, {}, (attr,)),
        attr,
    )

def HttpRequest__get_host(self, *args, **kwargs):
    try:
        return self.COOKIES[app_settings.COOKIE_NAME]
    except KeyError:
        return HttpRequest__get_host._get_host(self, *args, **kwargs)

def RequestFactory__generic(self, *args, **kwargs):
    response = RequestFactory__generic._generic(self, *args, **kwargs)

    try:
        url = urlsplit(response['Location'])
    except KeyError:
        return response

    try:
        match = resolve(url.path)
    except Resolver404:
        return response

    if isinstance(response, HttpResponseSwitchRedirect) or \
            match.func is redirect_:
        return self.get(url.path, QueryDict(url.query), follow=False)

    return response

def noop(*args, **kwargs):
    return
