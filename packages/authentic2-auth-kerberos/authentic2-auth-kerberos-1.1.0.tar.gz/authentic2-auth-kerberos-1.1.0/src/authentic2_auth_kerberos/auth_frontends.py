from django.utils.translation import gettext_noop
from django import forms

from . import app_settings, utils

class KerberosFrontend(object):
    def enabled(self):
        return app_settings.ENABLED

    def name(self):
        return gettext_noop('Kerberos')

    def id(self):
        return 'kerberos'

    def form(self):
        return forms.Form

    def post(self, request, form, nonce, next):
        return utils.redirect_next(request, 'kerberos-login', nonce=nonce)

    def template(self):
        return 'authentic2_auth_kerberos/login.html'

    def is_hidden(self, request):
        return 'a2_just_logged_out' not in request.COOKIES
