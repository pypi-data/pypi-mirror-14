from django.contrib.admin.options import InlineModelAdmin

from lazychoices.forms import LazyChoiceInlineFormSet

from .checks import LazyChoiceInlineModelAdminChecks


class LazyChoiceInlineModelAdminMixin(InlineModelAdmin):
    checks_class = LazyChoiceInlineModelAdminChecks
    formset = LazyChoiceInlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(LazyChoiceInlineModelAdminMixin, self).get_formset(request, obj, **kwargs)
        formset.lazy_model = self.lazy_model
        return formset
