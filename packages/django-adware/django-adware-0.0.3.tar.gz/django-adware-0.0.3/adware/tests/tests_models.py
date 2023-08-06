from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from ..models import AdSense
from .. import utils as util
from .. import defaults as defs

User = get_user_model()


class CommonTestCase(TestCase):
    """
    Model Tests.
    """
    site_value = (defs.ADWARE_DEFAULT_AD_CLIENT, defs.ADWARE_DEFAULT_AD_SLOT)
    user_value = ('ca-pub-905269603332983480', '3864455494')

    def setUp(self):
        user = User.objects.create(email='foo@bar.com')
        user.adsense.code = 'foobar'
        user.adsense.ad_client = 'ca-pub-905269603332983480'
        user.adsense.ad_slot='3864455494'
        user.adsense.active = True
        user.adsense.save()

    def test_user_is_active(self):
        user = User.objects.get(email='foo@bar.com')
        self.assertEqual(user.is_active, True)

    def test_adsense_is_active(self):
        user = User.objects.get(email='foo@bar.com')
        self.assertEqual(user.adsense.active, True)

    def test_adsense_get_percentage(self):
        user = User.objects.get(email='foo@bar.com')
        viewcount = 999
        percentage = user.adsense.get_percentage(viewcount)
        self.assertEqual(percentage, 30)

        viewcount = 4999
        percentage = user.adsense.get_percentage(viewcount)
        self.assertEqual(percentage, 40)

    def test_adsense_get_info_site(self):
        user = User.objects.get(email='foo@bar.com')
        user.adsense.percentage = 0
        info = user.adsense.get_info()
        self.assertEqual(info, self.site_value)

    def test_adsense_get_info_user(self):
        user = User.objects.get(email='foo@bar.com')
        user.adsense.percentage = 100
        info = user.adsense.get_info()
        self.assertEqual(info, self.user_value)

    def test_adsense_get_info_no_code(self):
        user = User.objects.get(email='foo@bar.com')
        user.adsense.percentage = 100
        user.adsense.code = ''
        info = user.adsense.get_info()
        self.assertEqual(info, self.site_value)

    def test_adsense_get_info_not_active(self):
        user = User.objects.get(email='foo@bar.com')
        user.adsense.percentage = 100
        user.adsense.active = False
        info = user.adsense.get_info()
        self.assertEqual(info, self.site_value)

    def test_adsense_get_info_suspended(self):
        user = User.objects.get(email='foo@bar.com')
        user.adsense.percentage = 100
        user.adsense.suspended = True
        info = user.adsense.get_info()
        self.assertEqual(info, self.site_value)
