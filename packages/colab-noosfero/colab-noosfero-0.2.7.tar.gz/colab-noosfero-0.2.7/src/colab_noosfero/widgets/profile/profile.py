from django.utils.translation import ugettext_lazy as _
from colab_noosfero.views import NoosferoProxyView, NoosferoProfileProxyView
from colab.widgets.profile_widget import ProfileWidget


class NoosferoProfileWidget(NoosferoProxyView, ProfileWidget):
    identifier = 'noosfero_profile'
    name = _('Social')
    app_name = 'colab_noosfero'

    def default_url(self, request):
        user = request.user.username
        return '{}/myprofile/{}/profile_editor/edit'.format(self.prefix, user)

    def dispatch(self, request, url):
        noosfero_proxy_view = NoosferoProfileProxyView()
        response = noosfero_proxy_view.dispatch(request, url)

        if response.status_code == 302:
            url = self.fix_url(self.default_url(request))
            request.method = 'GET'
            response = noosfero_proxy_view.dispatch(request, url)

        return response
