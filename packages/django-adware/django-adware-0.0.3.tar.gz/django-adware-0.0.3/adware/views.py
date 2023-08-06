from django.contrib import messages
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect

from toolware.utils.mixin import LoginRequiredMixin
from toolware.utils.mixin import CsrfProtectMixin
from toolware.utils.mixin import DeleteMixin

from .forms import AdSenseForm
from . import utils as util


class AdSenseView(LoginRequiredMixin, CsrfProtectMixin, UpdateView):
    """
    AdSense View
    """
    form_class = AdSenseForm
    success_url = reverse_lazy('adware:adsense_update')

    def get_template_names(self):
        template_name = util.get_template_path("adsense_form.html")
        return template_name

    def get_context_data(self, **kwargs):
        context = super(AdSenseView, self).get_context_data(**kwargs)
        context['adsense'] = self.object
        return context

    def get_object(self, queryset=None):
        ad = self.request.user.adsense
        return ad

    def form_valid(self, form):
        self.object = form.save()
        if self.object.code:
            messages.add_message(self.request, messages.SUCCESS, _('Your AdSense code was saved.'))
        return HttpResponseRedirect(self.get_success_url())
