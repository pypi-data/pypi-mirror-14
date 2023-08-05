from django.conf import settings
from django.template import Engine, Context
from django.utils.encoding import smart_unicode
from django.core.exceptions import MiddlewareNotUsed

from .utils import set_urlconf_from_host
from .app_settings import app_settings

class SubdomainMiddleware(object):
    """
    Adjust incoming request's urlconf based on `settings.SUBDOMAINS`.

    Overview
    ========

    This middleware routes requests to specific subdomains to different URL
    schemes ("urlconf").

    For example, if you own ``example.com`` but want to serve specific content
    at ``api.example.com` and ``beta.example.com``, add the following to your
    ``settings.py``:

        from dynamic_subdomains.subdomains import subdomain

        SUBDOMAINS = (
            subdomain(r'api', 'path.to.api.urls',
                name='api'),
            subdomain(r'beta', 'path.to.beta.urls',
                name='beta'),
        )

    This causes requests to ``{api,beta}.example.com`` to be routed to their
    corresponding urlconf. You can use your ``urls.py`` as a template for these
    urlconfs.

    Patterns are evaluated in order. If no subdomain pattern matches, the
    subdomain specified by ``settings.DEFAULT_SUBDOMAIN`` is used.

    Pattern format
    ==============

    The patterns on the left-hand side are regular expressions. For example,
    the following ``settings.SUBDOMAINS`` will route ``foo.example.com`` and
    ``bar.example.com`` to the same urlconf.

        SUBDOMAINS = (
            subdomain(r'(foo|bar)', 'path.to.urls',
                name='foo-or-bar'),
        )

    .. note:

      * Patterns are matched against the extreme left of the requested host

      * It is implied that all patterns end either with a literal full stop
        (ie. ".") or an end of line metacharacter.

      * As with all regular expressions, various metacharacters need quoting.

    Using regular expressions
    =========================

    Patterns as regular expressions allows setups to feature dynamic (or
    "wildcard") subdomain schemes:

        SUBDOMAINS = (
            subdomain(r'www', ROOT_URLCONF,
                name='static'),
            subdomain(r'\w+', 'path.to.custom_urls',
                name='wildcard'),
        )

    Here, requests to ``www.example.com`` will be routed as normal but a
    request to ``lamby.example.com`` is routed to ``path.to.custom_urls``.

    As subdomains are matched in order, we placed ``www`` first as it otherwise
    would have matched against ``\w+`` and thus routed to the wrong
    destination.

    Alternatively, we could have used negative lookahead:

        SUBDOMAINS = (
            subdomain(r'(?!www)\w+', 'path.to.custom_urls',
                name='wildcard'),
        )

    Callback methods to simplify dynamic subdomains
    ===============================================

    The previous section outlined using regular expressions to implement
    dynamic subdomains.

    However, inside every view referenced by the target urlconf we would have
    to parse the subdomain from ``request.get_host()`` and lookup its
    corresponding object instance, violating DRY. If these dynamic subdomains
    had a lot of views this would become particularly unwieldy.

    To remedy this, you can optionally specify a callback method to be called
    if your subdomain matches:

        SUBDOMAINS = (
            subdomain(r'www', ROOT_URLCONF,
                name='static'),
            subdomain(r'(?P<username>\w+)', 'path.to.custom_urls',
                callback='path.to.custom_fn', name='with-callback'),
        )

        [..]

        from django.shortcuts import get_object_or_404
        from django.contrib.auth.models import User

        def custom_fn(request, username):
            request.viewing_user = get_object_or_404(User, username=username)

    This example avoids the duplicated work in every view by attaching a
    ``viewing_user`` instance to the request object. Views referenced by the
    "dynamic" urlconf can now assume that this object exists.

    The custom method is called with the ``request`` object and any named
    captured arguments, similar to regular Django url processing.

    Callbacks may return either ``None`` or an ``HttpResponse`` object. If it
    returns ``None``, the request continues to be processed and the appropriate
    view is eventually called. If a callback returns an ``HttpResponse``
    object, that ``HttpResponse`` is returned to the client without any further
    processing.

    .. note:

        Callbacks are executed with the urlconf set to the second argument in
        the ``SUBDOMAINS`` list. For example, in the example above, the
        callback will be executed with the urlconf as ``path.to.custom_urls``
        and not the default urlconf.

        This can cause problems when reversing URLs within your callback as
        they may not be "visible" to ``django.core.urlresolvers.reverse`` as
        they are specified in (eg.) the default urlconf.

        To remedy this, specify the ``urlconf`` parameter when calling
        ``reverse``.

    Notes
    =====

      * When using dynamic subdomains based on user input, ensure users cannot
        specify names that conflict with static subdomains such as "www" or
        their subdomain will not be accessible.

      * Don't forget to add ``handler404`` and ``handler500`` entries for your
        custom urlconfs.
    """

    TAG = '</body>'
    TEMPLATE = """
        <script type="text/javascript">
            function dynamicSubdomains() {
                var val = prompt("Update host", '{{ request.get_host|escapejs }}');
                document.cookie = '{{ app_settings.COOKIE_NAME }}=' + val + '; expires=Tue, 19 Jan 2038 03:14:07 UTC;';
                window.location.reload();
            }
        </script>
        <style type="text/css">
            #dynamic-subdomains-toolbar {
                right: 0;
                bottom: 0;
                height: 36px;
                z-index: 99999;
                position: fixed;

                padding: 10px 16px 0 16px;
                background-color: #092e20;
                border-top-left-radius: 7px;

                color: white;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
            }
        </style>
        <div id="dynamic-subdomains-toolbar" onclick="dynamicSubdomains();">
            {{ request.build_absolute_uri }}
        </div>
    """

    def __init__(self):
        if not settings.SUBDOMAINS:
            raise MiddlewareNotUsed()

    def process_request(self, request):
        host = request.get_host()

        with set_urlconf_from_host(host) as (subdomain, kwargs):
            request.urlconf = subdomain['urlconf']

            return subdomain['_callback'](request, **kwargs)

    def process_response(self, request, response):
        if not app_settings.EMULATE:
            return response

        try:
            val = smart_unicode(response.content)
        except Exception:
            return response

        toolbar = Engine(debug=True).from_string(self.TEMPLATE).render(Context({
            'request': request,
            'app_settings': app_settings,
        }))

        idx = val.lower().rfind(self.TAG.lower())

        if idx >= 0:
            response.content = val[:idx] + toolbar + val[idx + len(self.TAG):]

        return response
