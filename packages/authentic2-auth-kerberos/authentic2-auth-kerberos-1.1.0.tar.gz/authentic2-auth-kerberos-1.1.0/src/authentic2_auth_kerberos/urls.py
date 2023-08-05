from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns('',
        url(r'^accounts/kerberos/login/$', views.login, name='kerberos-login'),
)
