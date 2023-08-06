import random

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.utils.encoding import python_2_unicode_compatible

from . import utils as util
from . import defaults as defs

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class AdSense(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        related_name="%(class)s",
        editable=False,
    )

    code = models.TextField(
        _("Adsense Code"),
        blank=True,
        null=True,
        help_text=_('Your Google "Responsive" Adsense Code.'),
    )

    ad_client = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )

    ad_slot = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    percentage = models.PositiveIntegerField(
        default=defs.ADWARE_MINIMUM_IMPRESSION_PERCENTAGE,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text=_('Ad impression percentage (1-100).'),
    )

    active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Active shows your ads.'),
    )

    suspended = models.BooleanField(
        _('suspended'),
        default=False,
        help_text=_('Suspended AdShare will not show ads. For admin use.'),
    )

    def __str__(self):
        return 'Adsense: {} [p:{}, a:{}]'.format(self.user.username, self.percentage, self.active)

    def get_percentage(self, view_count):
        percentage = util.get_percentage_per_view(self.percentage, view_count)
        return percentage

    def get_info(self, view_count=0):
        """
        Returns ad client/slot or ''
        """
        info = (defs.ADWARE_DEFAULT_AD_CLIENT, defs.ADWARE_DEFAULT_AD_SLOT)
        if self.user.is_active and self.active and not self.suspended:
            if self.code and self.ad_client and self.ad_slot:
                rand = random.randint(1, 100)
                percentage = self.get_percentage(view_count)
                if rand <= percentage:
                    info = (self.ad_client, self.ad_slot)
        return info
