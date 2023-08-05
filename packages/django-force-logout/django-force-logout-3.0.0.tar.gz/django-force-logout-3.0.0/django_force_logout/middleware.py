import time
import datetime

from django.contrib import auth

from . import app_settings
from .utils import from_dotted_path

class ForceLogoutMiddleware(object):
    SESSION_KEY = 'force-logout:last-login'

    def __init__(self):
        self.fn = app_settings.CALLBACK

        if not callable(self.fn):
            self.fn = from_dotted_path(self.fn)

        def callback(sender, user=None, request=None, **kwargs):
            if request:
                request.session[self.SESSION_KEY] = int(time.time())
        auth.signals.user_logged_in.connect(callback, weak=False)

    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        user_timestamp = self.fn(request.user)

        if user_timestamp is None:
            return

        try:
            timestamp = datetime.datetime.utcfromtimestamp(
                request.session[self.SESSION_KEY],
            )
        except KeyError:
            # May not have logged in since we started populating this key.
            return

        if timestamp > user_timestamp:
            return

        auth.logout(request)
