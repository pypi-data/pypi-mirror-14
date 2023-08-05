import logging

from django_kerberos.views import NegotiateView

from authentic2.models import AuthenticationEvent
from authentic2 import utils

__ALL_ = [ 'login' ]

class A2NegotiateView(NegotiateView):
    def __init__(self, *args, **kwargs):
        super(A2NegotiateView, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def login_user(self, request, user):
        utils.login(request, user, 'kerberos')

login = A2NegotiateView.as_view()
