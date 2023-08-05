from django.forms import TypedChoiceField


class LazyChoiceField(TypedChoiceField):
    def __init__(self, choices_name, model=None, empty_label='---------', *args, **kwargs):
        super(LazyChoiceField, self).__init__(*args, **kwargs)
        self.choices_name = choices_name
        self.empty_label = empty_label
        self.model = model

    def __deepcopy__(self, memo):
        result = super(LazyChoiceField, self).__deepcopy__(memo)
        result.model = result.model
        return result

    def _get_model(self):
        return self._model

    def _set_model(self, model):
        self._model = model
        self.choices = self._get_model_choices(model)

    model = property(_get_model, _set_model)

    def _get_model_choices(self, model):
        if self.required and (self.initial is not None):
            first_choice = []
        else:
            first_choice = [(self.empty_value, self.empty_label)]
        return first_choice + getattr(model, self.choices_name, [])
