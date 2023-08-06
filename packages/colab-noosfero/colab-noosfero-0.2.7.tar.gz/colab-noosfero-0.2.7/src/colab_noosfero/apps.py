from colab.plugins.utils.apps import ColabPluginAppConfig
from colab.signals.signals import register_signal
from django.contrib.auth.signals import user_logged_in, user_logged_out
from colab_noosfero.tasks import authenticate_user, logout_user


class NoosferoPluginAppConfig(ColabPluginAppConfig):
    name = 'colab_noosfero'
    verbose_name = 'Noosfero Plugin'
    namespace = 'noosfero'

    registered_signals = ['community_creation', 'community_updated']
    short_name = 'noosfero'

    def register_signal(self):
        register_signal(self.short_name, self.registered_signals)

    def ready(self):
        import colab_noosfero.signals  # NOQA

    def connect_signal(self):
        user_logged_in.connect(authenticate_user)
        user_logged_out.connect(logout_user)
