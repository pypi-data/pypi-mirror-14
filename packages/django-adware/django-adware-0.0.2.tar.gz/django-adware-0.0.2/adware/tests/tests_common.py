from django.http import HttpRequest
from django.test import TestCase

from .. import utils as util


class CommonTestCase(TestCase):
    """
    Common Tests.
    """
    def test_attributes(self):
        client = 'ca-pub-905269603333983480'
        slot = '3864455294'
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
