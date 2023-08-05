from django.contrib.admin.checks import must_be, must_inherit_from

from lazychoices.compat import InlineModelAdminChecks
from lazychoices.models import LazyChoiceModelMixin


class LazyChoiceInlineModelAdminChecks(InlineModelAdminChecks):
    def _check_lazy_model(self, obj):
        if not hasattr(obj, 'lazy_model'):
            return must_be('defined', option='lazy_model', obj=obj, id='lazychoices.E101')
        elif not issubclass(obj.lazy_model, LazyChoiceModelMixin):
            return must_inherit_from(parent='LazyChoiceModelMixin', option='lazy_model',
                                     obj=obj, id='lazychoices.E102')
        else:
            return []
