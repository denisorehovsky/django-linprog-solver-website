from django import forms
from django.utils.translation import ugettext_lazy as _

from .exceptions import SimplexInitException


class SimplexInitForm(forms.Form):
    variables = forms.ChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)]
    )
    conditions = forms.ChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)]
    )


class SimplexSolveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.variables, self.conditions = self._process_variables_and_conditions(
            kwargs.pop('variables', None), kwargs.pop('conditions', None)
        )
        super().__init__(*args, **kwargs)
        self._set_simplex_form_fields()

    def _process_variables_and_conditions(self, variables, conditions):
        try:
            variables, conditions = int(variables), int(conditions)
        except:
            raise SimplexInitException(_('Please define the number of variables and conditions'))

        if 1 <= variables <= 10 and 1 <= conditions <= 10:
            return variables, conditions
        else:
            raise SimplexInitException(_('The number of variables and conditions should be between 1 and 10'))

    def _set_simplex_form_fields(self):
        for i in range(1, self.variables + 1):
            func_coeff = 'func_coeff_{}'.format(i)
            self.fields[func_coeff] = forms.FloatField()

        self.fields['tendency'] = forms.ChoiceField(
            initial='max', choices=[('max', 'max'), ('min', 'min')]
        )

        for i in range(1, self.conditions + 1):
            cond_operator = 'cond_operator_{}'.format(i)
            self.fields[cond_operator] = forms.ChoiceField(
                initial='<=', choices=[('<=', '<='), ('>=', '>='), ('=', '=')]
            )

            cond_const = 'cond_const_{}'.format(i)
            self.fields[cond_const] = forms.FloatField()

            for k in range(1, self.variables + 1):
                cond_coeff = 'cond_coeff_{}_{}'.format(i, k)
                self.fields[cond_coeff] = forms.FloatField()
