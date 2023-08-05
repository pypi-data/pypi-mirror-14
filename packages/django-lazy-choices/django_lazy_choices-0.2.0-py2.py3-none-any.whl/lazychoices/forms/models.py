from django.forms import BaseInlineFormSet, ModelForm

from .fields import LazyChoiceField


class LazyChoiceInlineFormSet(BaseInlineFormSet):
    lazy_model = None

    def _construct_form(self, i, **kwargs):
        form = super(LazyChoiceInlineFormSet, self)._construct_form(i, **kwargs)
        form.lazy_model = self.lazy_model
        return form

    @property
    def empty_form(self):
        form = super(LazyChoiceInlineFormSet, self).empty_form
        form.lazy_model = self.lazy_model
        return form


class LazyChoiceModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LazyChoiceModelForm, self).__init__(*args, **kwargs)
        self.lazy_model = self.instance._meta.model

    def _get_lazy_model(self):
        return self._lazy_model

    def _set_lazy_model(self, lazy_model):
        self._lazy_model = lazy_model
        for field_name in self.fields:
            formfield = self.fields[field_name]
            if isinstance(formfield, LazyChoiceField):
                formfield.model = lazy_model

    lazy_model = property(_get_lazy_model, _set_lazy_model)
