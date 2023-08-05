from django.http import HttpResponseRedirect, HttpResponseForbidden

from .app_settings import app_settings

def redirect_(request, host):
    if not app_settings.EMULATE:
        return HttpResponseForbidden()

    response = HttpResponseRedirect(request.META.get('QUERY_STRING', '') or '/')
    response.set_cookie(app_settings.COOKIE_NAME, host)
    response.status_code = 307 # Re-submit POST requests

    return response
