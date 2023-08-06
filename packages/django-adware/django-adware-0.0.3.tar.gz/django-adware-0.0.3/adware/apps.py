from django.conf import settings
from django.db.models import signals
from django.apps import AppConfig as DjangoAppConfig

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class AppConfig(DjangoAppConfig):
    """
    Configuration entry point for the adware app
    """
    label = name = 'adware'
    verbose_name = "adware"

    def ready(self):
        """
        App is imported and ready, so bootstrap it.
        """
        from . import receivers as rcv

        signals.post_save.connect(rcv.create_ad, sender=AUTH_USER_MODEL)
