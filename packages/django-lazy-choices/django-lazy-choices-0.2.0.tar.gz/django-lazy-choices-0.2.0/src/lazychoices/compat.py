import django
from django.contrib.admin.checks import InlineModelAdminChecks as BaseInlineModelAdminChecks


def get_empty_value_display(model_admin):
    if django.VERSION >= (1, 9):
        return model_admin.get_empty_value_display()
    else:
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        return EMPTY_CHANGELIST_VALUE


if django.VERSION >= (1, 9):
    class InlineModelAdminChecks(BaseInlineModelAdminChecks):
        def check(self, inline_obj, **kwargs):
            errors = super(InlineModelAdminChecks, self).check(inline_obj)
            errors.extend(self._check_lazy_model(inline_obj))
            return errors
else:
    class InlineModelAdminChecks(BaseInlineModelAdminChecks):
        def check(self, cls, parent_model, **kwargs):
            errors = super(InlineModelAdminChecks, self).check(cls, parent_model, **kwargs)
            errors.extend(self._check_lazy_model(cls))
            return errors
