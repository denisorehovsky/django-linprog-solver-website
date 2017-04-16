from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit

from scipy.optimize import linprog

from .exceptions import SimplexInitException


class SimplexInitForm(forms.Form):
    variables = forms.ChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)]
    )
    conditions = forms.ChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)]
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(Field('variables'), css_class='col-md-offset-3 col-sm-3 col-md-2 text-center'),
            Div(Field('conditions'), css_class='col-sm-3 col-md-2 text-center'),
            Div(css_class='clearfix'),
            Div(Submit('submit', _('Next step')), css_class='col-md-offset-3'),
        )
        super().__init__(*args, **kwargs)


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

    def solve(self):
        sign = 1 if self.cleaned_data['tendency'] == 'min' else -1
        c = [self.cleaned_data['func_coeff_{}'.format(i)] * sign
             for i in range(1, self.variables + 1)]

        A_ub, A_eq, b_ub, b_eq = None, None, None, None
        for i in range(1, self.conditions + 1):
            operator = self.cleaned_data['cond_operator_{}'.format(i)]
            if operator == '<=' or operator == '>=':
                sign = 1 if operator == '<=' else -1
                if b_ub is None:
                    b_ub = []
                if A_ub is None:
                    A_ub = []
                b_ub.append(sign * self.cleaned_data['cond_const_{}'.format(i)])
                A_ub.append([sign * self.cleaned_data['cond_coeff_{}_{}'.format(i, k)]
                             for k in range(1, self.variables + 1)])
            else:
                if b_eq is None:
                    b_eq = []
                if A_eq is None:
                    A_eq = []
                b_eq.append(self.cleaned_data['cond_const_{}'.format(i)])
                A_eq.append([self.cleaned_data['cond_coeff_{}_{}'.format(i, k)]
                             for k in range(1, self.variables + 1)])

        result = linprog(c, A_ub, b_ub, A_eq, b_eq)
        if self.cleaned_data['tendency'] == 'max':
            result['fun'] = -result['fun']

        return result
