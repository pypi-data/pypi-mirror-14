from django.http import HttpRequest
from django.test import TestCase

from .. import utils as util
from .. import defaults as defs


class CommonTestCase(TestCase):
    """
    Common Tests.
    """
    def test_attributes(self):
        client = 'ca-pub-905269603332983480'
        slot = '3864455494'
        ad = """ <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="{}"
                 data-ad-slot="{}"
                 data-ad-format="auto"></ins>
            <script>
            </script>
        """
        info = util.get_adsense_attribute(ad.format(client, slot))
        self.assertEqual(info, (client, slot))

    def test_percentage_per_view_999(self):
        percentage = 30
        viewcount = 999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(percentage, value)

    def test_percentage_per_view_4999(self):
        percentage = 30
        viewcount = 4999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(percentage + 10, value)

    def test_percentage_per_view_9999(self):
        percentage = 30
        viewcount = 9999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(percentage + 20, value)

    def test_percentage_per_view_14999(self):
        percentage = 30
        viewcount = 14999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(percentage + 30, value)

    def test_percentage_per_view_19999(self):
        percentage = 30
        viewcount = 19999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(percentage + 40, value)

    def test_percentage_per_view_29999(self):
        percentage = 30
        viewcount = 29999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(percentage + 50, value)

    def test_percentage_per_view_reward_cap(self):
        percentage = 60
        viewcount = 50000
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(defs.ADWARE_MAX_PERCENTAGE_REWARD, value)

    def test_percentage_per_view_reward_override(self):
        percentage = 90
        viewcount = 999
        value = util.get_percentage_per_view(percentage, viewcount)
        self.assertEqual(90, value)
