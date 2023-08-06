from django import template
from django.conf import settings

from .. import defaults as defs

register = template.Library()


@register.assignment_tag(takes_context=True)
def adsense_info(context, user=None, view_count=0):
    """
    Returns AdSense info
    """
    if user:
        info = user.adsense.get_info(view_count)
    else:
        info = (defs.ADWARE_DEFAULT_AD_CLIENT, defs.ADWARE_DEFAULT_AD_SLOT)
    return info
