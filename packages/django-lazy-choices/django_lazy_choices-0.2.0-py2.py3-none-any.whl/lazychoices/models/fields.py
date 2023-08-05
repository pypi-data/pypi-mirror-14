from django.core import checks, exceptions
from django.db.models import BLANK_CHOICE_DASH, CharField
from django.utils import six
from django.utils.functional import curry
from django.utils.itercompat import is_iterable
from django.utils.text import capfirst

from lazychoices import forms

from .mixins import LazyChoiceModelMixin


class LazyChoiceField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', BLANK_CHOICE_DASH)
        kwargs.setdefault('max_length', 25)
        super(LazyChoiceField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(LazyChoiceField, self).check(**kwargs)
        errors.extend(self._check_model())
        for subclass in self.model.__subclasses__():
            errors.extend(self._check_choices(subclass))
        return errors

    def _check_choices(self, klass=None):
        klass = klass or self.model
        if hasattr(klass, self.choices_name):
            choices = getattr(klass, self.choices_name)
            if (isinstance(choices, six.string_types) or not is_iterable(choices)):
                return [
                    checks.Error(
                        "'{0}' must be an iterable (e.g., a list or tuple).".format(self.choices_name),
                        hint=None,
                        obj=klass,
                        id='lazychoices.E001',
                    )
                ]
            elif any(isinstance(choice, six.string_types) or
                     not is_iterable(choice) or len(choice) != 2
                     for choice in choices):
                return [
                    checks.Error(
                        ("'{0}' must be an iterable containing "
                         "(actual value, human readable name) tuples.").format(self.choices_name),
                        hint=None,
                        obj=klass,
                        id='lazychoices.E002',
                    )
                ]
            else:
                return []
        else:
            return []

    def _check_model(self):
        if not issubclass(self.model, LazyChoiceModelMixin):
            return [
                checks.Error(
                    "The model must inherit from 'LazyChoiceModelMixin'.",
                    hint=None,
                    obj=self.model,
                    id='lazychoices.E003',
                )
            ]
        else:
            return []

    def validate(self, value, model_instance):
        choices = getattr(model_instance, self.choices_name, [])
        if choices and value not in self.empty_values:
            for option_key, option_value in choices:
                if isinstance(option_value, (list, tuple)):
                    for optgroup_key, optgroup_value in option_value:
                        if value == optgroup_key:
                            return
                elif value == option_key:
                    return

            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

    def set_attributes_from_name(self, name):
        super(LazyChoiceField, self).set_attributes_from_name(name)
        self.choices_name = '{0}_CHOICES'.format(self.name.upper())

    def contribute_to_class(self, cls, name):
        super(LazyChoiceField, self).contribute_to_class(cls, name)
        if hasattr(cls, '_get_LAZYFIELD_display'):
            setattr(cls, 'get_{0}_display'.format(self.name), curry(cls._get_LAZYFIELD_display, field=self))

    def formfield(self, form_class=None, **kwargs):
        defaults = {
            'help_text': self.help_text,
            'label': capfirst(self.verbose_name),
            'model': self.model,
            'required': not self.blank,
        }

        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()

        defaults['choices_name'] = self.choices_name
        defaults['coerce'] = self.to_python

        if self.null:
            defaults['empty_value'] = None

        # Many of the subclass-specific formfield arguments (min_value,
        # max_value) don't apply for choice fields, so be sure to only pass
        # the values that TypedChoiceField will understand.
        for k in list(kwargs):
            if k not in ['coerce', 'empty_label', 'empty_value', 'choices_name',
                         'model', 'required', 'widget', 'label', 'initial',
                         'help_text', 'error_messages', 'show_hidden_initial']:
                del kwargs[k]

        defaults.update(kwargs)
        if form_class is None:
            form_class = forms.LazyChoiceField
        return form_class(**defaults)
