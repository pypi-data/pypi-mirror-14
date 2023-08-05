from django.contrib.admin import ChoicesFieldListFilter
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from lazychoices.compat import get_empty_value_display
from lazychoices.utils import flatten_choices


class LazyChoicesFieldListFilter(ChoicesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_choices = flatten_choices(self.field_choices(field, request, model_admin))
        self.lookup_kwarg_isnull = '{0}__isnull'.format(field_path)
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull)
        super(LazyChoicesFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.empty_value_display = get_empty_value_display(model_admin)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def field_choices(self, field, request, model_admin):
        return getattr(model_admin.model, field.choices_name, [])

    def choices(self, cl):
        yield {
            'selected': self.lookup_val is None and not self.lookup_val_isnull,
            'query_string': cl.get_query_string({}, [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': smart_text(lookup) == self.lookup_val,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: lookup,
                }, [self.lookup_kwarg_isnull]),
                'display': title,
            }
        if self.field.null:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }
