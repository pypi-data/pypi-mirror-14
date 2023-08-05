from django import forms
from django.utils.translation import ugettext_lazy as _

from toolware.utils.mixin import CleanSpacesMixin

from .models import AdSense
from . import utils as util


class AdSenseForm(CleanSpacesMixin, forms.ModelForm):
    """
    Custom AdSense Update Form, Simple.
    """
    def __init__(self, *args, **kwargs):
        super(AdSenseForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = ''

    def clean_code(self):
        code = self.cleaned_data.get('code', '')
        if code:
            ad_client, ad_slot = util.get_adsense_attribute(code)
            if not ad_client:
                raise forms.ValidationError(_("Invalid AdSense Code. Unable to extract data-ad-client attribute."))
            if not ad_slot:
                raise forms.ValidationError(_("Invalid AdSense Code. Unable to extract data-ad-slot attribute."))
        return code

    class Meta:
        model = AdSense
        fields = ('code', 'active')

    def save(self, commit=True):
        instance = super(AdSenseForm, self).save(commit=False)
        instance.ad_client, instance.ad_slot = util.get_adsense_attribute(self.cleaned_data['code'])
        if commit:
            instance.save()
        return instance
