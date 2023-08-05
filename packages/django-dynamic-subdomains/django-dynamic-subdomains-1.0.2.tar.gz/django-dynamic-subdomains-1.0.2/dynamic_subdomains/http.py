from django.http import HttpResponseRedirect

from .app_settings import app_settings

class HttpResponseSwitchRedirect(HttpResponseRedirect):
    status_code = 307 # Re-submit POST requests

    def __init__(self, host, path, *args, **kwargs):
        super(HttpResponseSwitchRedirect, self).__init__(path, *args, **kwargs)

        self.set_cookie(app_settings.COOKIE_NAME, host)
