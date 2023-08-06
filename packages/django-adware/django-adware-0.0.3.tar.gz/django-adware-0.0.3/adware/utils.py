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


def get_percentage_per_view(percentage, view_count):
    """
    Calculates new ad impression percentage based on total view count.
    """
    if not defs.ADWARE_IMPRESSION_REWARD_ENABLED:
        return percentage

    # special case when user is awarded > 80 %
    if percentage >= 80:
        return percentage

    # reward good content by number views
    new_percentage = percentage
    for item in defs.ADWARE_IMPRESSION_REWARD:
        level, reward = item
        if view_count >= level:
            new_percentage = percentage + reward
            break

    # cap max reward
    if new_percentage > defs.ADWARE_MAX_PERCENTAGE_REWARD:
        new_percentage = defs.ADWARE_MAX_PERCENTAGE_REWARD
    return new_percentage
