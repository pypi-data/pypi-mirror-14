import re
import urllib

from django.utils.encoding import force_unicode
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.regex_helper import normalize

from .utils import get_subdomain
from .app_settings import app_settings

def reverse_subdomain(subdomain_name, args=(), kwargs=None):
    if args and kwargs:
        raise ValueError("Don't mix *args and **kwargs in call to reverse()!")

    if kwargs is None:
        kwargs = {}

    subdomain = get_subdomain(subdomain_name)

    unicode_args = [force_unicode(x) for x in args]
    unicode_kwargs = dict([(k, force_unicode(v)) for (k, v) in kwargs.items()])

    for result, params in normalize(subdomain['regex']):
        if args:
            if len(args) != len(params):
                continue
            candidate = result % dict(zip(params, unicode_args))
        else:
            if set(kwargs.keys()) != set(params):
                continue
            candidate = result % unicode_kwargs

        if re.match(subdomain['regex'], candidate, re.UNICODE):
            return candidate

    raise NoReverseMatch(
        "Reverse subdomain for '%s' with arguments '%s' and keyword arguments "
        "'%s' not found." % (subdomain_name, args, kwargs)
    )

def reverse_crossdomain_part(subdomain_name, path, subdomain_args=(), subdomain_kwargs=None):
    if subdomain_kwargs is None:
        subdomain_kwargs = {}

    domain_part = reverse_subdomain(
        subdomain_name,
        args=subdomain_args,
        kwargs=subdomain_kwargs,
    )

    if app_settings.EMULATE:
        url = '%s%s' % (
            app_settings.EMULATE_BASE_URL,
            reverse('dynamic-subdomains:redirect', args=(domain_part,)),
        )

        if path != '/':
            url += '?%s' % urllib.quote(path)

        return url

    return u'//%s%s' % (domain_part, path)

def reverse_path(subdomain_name, view, args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}

    subdomain = get_subdomain(subdomain_name)

    return reverse(
        view,
        args=args,
        kwargs=kwargs,
        urlconf=subdomain['urlconf'],
    )

def reverse_crossdomain(subdomain_name, view, subdomain_args=(), subdomain_kwargs=None, view_args=(), view_kwargs=None):
    path = reverse_path(subdomain_name, view, view_args, view_kwargs)

    return reverse_crossdomain_part(
        subdomain_name,
        path,
        subdomain_args,
        subdomain_kwargs,
    )
