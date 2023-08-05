from django.apps import AppConfig


class Authentic2AuthKerberosConfig(AppConfig):
    name = 'authentic2_auth_kerberos'
    label = 'authentic2_auth_kerberos'

    def ready(self):
        # patch authentic2.backends.ldap_backend.LDAPBackend for keys specific to Kerberos support
        from . import backends
