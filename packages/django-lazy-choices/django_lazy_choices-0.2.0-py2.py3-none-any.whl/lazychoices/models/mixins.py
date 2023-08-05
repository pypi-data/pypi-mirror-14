from django.utils.encoding import force_text

from lazychoices.utils import flatten_choices


class LazyChoiceModelMixin(object):
    def _get_LAZYFIELD_display(self, field):
        choices = getattr(self, field.choices_name, [])
        value = getattr(self, field.attname)
        return force_text(dict(flatten_choices(choices)).get(value, value), strings_only=True)
