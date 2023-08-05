import os

from bs4 import BeautifulSoup

from . import defaults as defs


def get_template_path(name):
    """
    Given a template name, it returns the relative path from the template dir.
    """
    path = os.path.join(defs.ADWARE_TEMPLATE_BASE_DIR, name)
    return path


def get_adsense_attribute(html):
    ad_client = ''
    ad_slot = ''
    if html:
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find('ins')
        ad_client = tag.get('data-ad-client', '')
        ad_slot = tag.get('data-ad-slot', '')
    return ad_client, ad_slot
