import logging
import pytest

from ldaptools.slapd import Slapd


pytestmark = pytest.mark.django_db

@pytest.fixture
def slapd(request, settings):
    slapd = Slapd(ldap_url=getattr(request, 'param', None))
    slapd.add_ldif('''dn: uid=john.doe,o=orga
objectClass: inetOrgPerson
cn: John Doe
sn: Doe
mail: john.doe@example.com
uid: john.doe
uid: john.doe@entrouvert.com
''')
    settings.LDAP_AUTH_SETTINGS = [
        {
            'url': [slapd.ldap_url],
            'basedn': 'o=orga',
            'use_tls': False,
        }
    ]
    return slapd

def test_authenticate_no_principal_filter(slapd):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    backend = A2LdapKerberosBackend()
    assert backend.authenticate(principal='john.doe@ENTROUVERT.COM') is None

def test_authenticate_success(slapd, settings, django_user_model, caplog):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    User = django_user_model
    settings.LDAP_AUTH_SETTINGS[0]['principal_filter'] = 'uid={username}'
    backend = A2LdapKerberosBackend()
    with caplog.atLevel(logging.INFO):
        assert not backend.authenticate(principal='john.doe@ENTROUVERT.COM') is None
    user = User.objects.get()
    assert user.username == 'john.doe@ldap'
    assert user.email == 'john.doe@example.com'
    assert not caplog.records()


def test_authenticate_principal_filter_with_realm(slapd, settings, django_user_model, caplog):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    User = django_user_model
    settings.LDAP_AUTH_SETTINGS[0]['principal_filter'] = 'uid={username}@{realm}'
    backend = A2LdapKerberosBackend()
    with caplog.atLevel(logging.INFO):
        assert not backend.authenticate(principal='john.doe@ENTROUVERT.COM') is None
    user = User.objects.get()
    assert user.username == 'john.doe@ldap'
    assert user.email == 'john.doe@example.com'
    assert not caplog.records()


def test_authenticate_bad_principal_filter(slapd, settings, django_user_model, caplog):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    User = django_user_model
    settings.LDAP_AUTH_SETTINGS[0]['principal_filter'] = 'uid={user}'
    backend = A2LdapKerberosBackend()
    with caplog.atLevel(logging.INFO):
        assert backend.authenticate(principal='john.doe@ENTROUVERT.COM') is None
    assert len(caplog.records()) == 1
    assert 'principal_filter does not' in caplog.text()


def test_authenticate_limit_to_realm_failure(slapd, settings, django_user_model, caplog):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    User = django_user_model
    settings.LDAP_AUTH_SETTINGS[0]['principal_filter'] = 'uid={username}'
    settings.LDAP_AUTH_SETTINGS[0]['limit_to_realm'] = True
    backend = A2LdapKerberosBackend()
    with caplog.atLevel(logging.INFO):
        assert backend.authenticate(principal='john.doe@ENTROUVERT.COM') is None
    assert not caplog.records()


def test_authenticate_limit_to_realm_success(slapd, settings, django_user_model):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    User = django_user_model
    settings.LDAP_AUTH_SETTINGS[0]['principal_filter'] = 'uid={username}'
    settings.LDAP_AUTH_SETTINGS[0]['limit_to_realm'] = True
    settings.LDAP_AUTH_SETTINGS[0]['realm'] = 'ENTROUVERT.COM'
    backend = A2LdapKerberosBackend()
    assert not backend.authenticate(principal='john.doe@ENTROUVERT.COM') is None
    user = User.objects.get()
    assert user.username == 'john.doe@ENTROUVERT.COM'


def test_authenticate_limit_to_realm_success(slapd, settings, django_user_model, caplog):
    from authentic2_auth_kerberos.backends import A2LdapKerberosBackend

    User = django_user_model
    settings.LDAP_AUTH_SETTINGS[0]['principal_filter'] = 'uid={username}'
    backend = A2LdapKerberosBackend()
    with caplog.atLevel(logging.INFO):
        assert backend.authenticate(principal='foo.bar@ENTROUVERT.COM') is None
    assert len(caplog.records()) == 1
    assert 'principal foo.bar@ENTROUVERT.COM not found' in caplog.text()
