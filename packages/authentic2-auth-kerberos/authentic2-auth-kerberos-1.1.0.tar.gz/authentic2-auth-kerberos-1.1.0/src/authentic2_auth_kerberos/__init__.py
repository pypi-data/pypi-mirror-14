default_app_config = 'authentic2_auth_kerberos.apps.Authentic2AuthKerberosConfig'


class Plugin(object):
    def get_before_urls(self):
        from . import urls
        return urls.urlpatterns

    def get_apps(self):
        return [__name__, 'django_kerberos']

    def get_authentication_backends(self):
        return ['authentic2_auth_kerberos.backends.A2LdapKerberosBackend',
                'authentic2_auth_kerberos.backends.A2KerberosBackend']

    def get_auth_frontends(self):
        return ['authentic2_auth_kerberos.auth_frontends.KerberosFrontend']
