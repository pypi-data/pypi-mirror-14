from django.http import HttpResponseForbidden

from .http import HttpResponseSwitchRedirect
from .app_settings import app_settings

def redirect_(request, host):
    if not app_settings.EMULATE:
        return HttpResponseForbidden()

    return HttpResponseSwitchRedirect(
        host,
        request.META.get('QUERY_STRING', '') or '/',
    )
