from colab_noosfero.views import NoosferoProxyView
from urllib3.exceptions import MaxRetryError
import logging
logger = logging.getLogger(__name__)


def authenticate_user(sender, user, request, **kwargs):
    proxy_view = NoosferoProxyView()
    try:
        noosfero_response = proxy_view.dispatch(request, '/')
    except MaxRetryError:
        logger.info("Couldn't connect to noosfero")
        return

    if noosfero_response.status_code == 200:
        session = noosfero_response.cookies.get('_noosfero_session').value
        request.COOKIES.set('_noosfero_session', session)


def logout_user(sender, user, request, **kwargs):
    request.COOKIES.delete('_noosfero_session')
