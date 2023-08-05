import logging

try:
    import ldap
except ImportError:
    ldap = None

from django.core.exceptions import ImproperlyConfigured
from django_kerberos.backends import KerberosBackend
from authentic2.backends.ldap_backend import LDAPBackend
from authentic2.ldap_utils import FilterFormatter
from authentic2.user_login_failure import user_login_success

from . import app_settings


class A2KerberosBackend(KerberosBackend):
    def __init__(self):
        super(A2KerberosBackend, self).__init__()
        self.logger = logging.getLogger(__name__)

    def username_from_principal(self, principal):
        if app_settings.REALM:
            username, domain = principal.rsplit('@', 1)
            return '{0}@{1}'.format(username, app_settings.REALM)
        return super(A2KerberosBackend, self).username_from_principal(principal)

    def should_create_user(self):
        return app_settings.CREATE_USER

    def provision_user(self, principal, user):
        pass

    def authenticate(self, principal=None, **kwargs):
        if not app_settings.ENABLED:
            return
        if not app_settings.DJANGO_BACKEND:
            return
        return super(A2KerberosBackend, self).authenticate(principal=principal, **kwargs)

    def get_saml2_authn_context(self):
        import lasso
        return lasso.SAML2_AUTHN_CONTEXT_KERBEROS

# Allow new parameter
LDAPBackend._DEFAULTS['principal_filter'] = None
LDAPBackend._VALID_CONFIG_KEYS.append('principal_filter')


class A2LdapKerberosBackend(LDAPBackend):
    def authenticate(self, principal=None, **kwargs):
        logger = logging.getLogger(__name__)

        if not app_settings.ENABLED:
            return
        if not app_settings.LDAP_BACKEND:
            return
        if not principal:
            return
        if principal.count('@') != 1:
            logger.warning(u'maformed principal %r', principal)
            return
        username, realm = principal.split('@')
        config = self.get_config()
        if not config:
            return
        if not ldap:
            raise ImproperlyConfigured('ldap is not available')

        for block in config:
            user = self.authenticate_block(block, username, realm, logger)
            if user:
                return user

    def authenticate_block(self, block, username, realm, logger):
        if not block['principal_filter']:
            return
        if block['limit_to_realm'] and realm != block['realm']:
            return
        if not '{username}' in block['principal_filter']:
            logger.warning('principal_filter does not contain the {username} pattern: %r',
                           block['principal_filter'])
            return

        user_basedn = block.get('user_basedn') or block['basedn']
        principal_filter = FilterFormatter().format(block['principal_filter'], username=username,
                                                    realm=realm)
        for conn in self.get_connections(block):
            try:
                results = conn.search_s(user_basedn, ldap.SCOPE_SUBTREE, principal_filter,
                                        self.get_ldap_attributes_names(block))
                results = [(dn, self.normalize_ldap_results(attrs)) for dn, attrs in results if dn]
                if not results and block['replicas']:
                    break
                if len(results) > 1:
                    logger.error('looking up principal %s@%s returned more than 1 user for %s',
                                 username, realm, block['url'])
                    return
                dn, attrs = results[0]
                attrs['dn'] = dn
                return self._return_user(dn, None, conn, block, attributes=attrs)
            except ldap.NO_SUCH_OBJECT:
                if block['replicas']:
                    logger.warning('principal filter failed with NO_SUCH_OBJECT: %r',
                                   principal_filter)
                    return
            except ldap.CONNECT_ERROR:
                logger.error('connection to %r failed, did you forget to declare the TLS '
                             'certificate in /etc/ldap/ldap.conf ?', block['url'])
            except ldap.TIMEOUT:
                logger.error('connection to %r timed out', block['url'])
            except ldap.SERVER_DOWN:
                logger.error('ldap authentication error: %r is down', block['url'])
        # Not found
        logger.info('principal %s@%s not found in %s', username, realm, block['url'])

    def get_saml2_authn_context(self):
        import lasso
        return lasso.SAML2_AUTHN_CONTEXT_KERBEROS
