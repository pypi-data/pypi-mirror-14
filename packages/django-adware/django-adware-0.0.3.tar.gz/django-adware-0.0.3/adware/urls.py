from django.conf import settings
from django.conf.urls import url
from django.conf.urls import patterns

from .views import *
from . import defaults as defs


urlpatterns = [

    url(
        r'^update$',
        AdSenseView.as_view(),
        name='adsense_update'
    ),

]
