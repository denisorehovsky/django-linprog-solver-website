from collections import defaultdict

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, Submit

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
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_action = 'simplex:solve'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(Field('variables'), css_class='col-md-offset-4 col-sm-3 col-md-2 text-center'),
            Div(Field('conditions'), css_class='col-sm-3 col-md-2 text-center'),
            Div(css_class='clearfix'),
            Submit('submit', _('Next step'), css_class='col-md-offset-4'),
        )


class SimplexSolveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.variables, self.conditions = self._process_variables_and_conditions(
            kwargs.pop('variables', None), kwargs.pop('conditions', None)
        )

        super().__init__(*args, **kwargs)
        self._set_simplex_form_fields()

        for __, field in self.fields.items():
            field.label = False

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'simplex:solve'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        self.helper.layout = Layout(
            Fieldset(
                'Objective function',
                *self._get_field_names_of_objective_function_coefficients(),
                'tendency',
            ),
            HTML('<div style="margin-top:75px;"></div>'),
            Fieldset(
                'Conditions',
                *[Div(*cond_coeffs, operator_field_name, const_field_name)
                  for cond_coeffs, operator_field_name, const_field_name in self._get_field_names_of_conditions()]
            ),
            HTML('<div style="margin-top:50px;"></div>'),
            Submit('submit', _('Next step')),
        )

    def _process_variables_and_conditions(self, variables: object, conditions: object) -> (int, int):
        try:
            variables, conditions = int(variables), int(conditions)
        except:
            raise SimplexInitException(_('Please define the number of variables and conditions'))

        if 1 <= variables <= 10 and 1 <= conditions <= 10:
            return variables, conditions
        else:
            raise SimplexInitException(_('The number of variables and conditions should be between 1 and 10'))

    def _get_field_names_of_objective_function_coefficients(self) -> list:
        """
        Gets names for the objective function coefficient fields
        depending on the number of `variables`.

        :Example: ['func_coeff_1', 'func_coeff_2', 'func_coeff_3']
        """
        return ['func_coeff_{}'.format(v) for v in range(1, self.variables + 1)]

    def _get_field_names_of_condition_coefficients(self) -> list:
        """
        Gets names for the condition coefficient fields
        depending on the number of `variables` and `conditions`.

        :Example: [['cond_coeff_1_1', 'cond_coeff_1_2'],
                   ['cond_coeff_2_1', 'cond_coeff_2_2']]
        """
        return [['cond_coeff_{}_{}'.format(c, v) for v in range(1, self.variables + 1)]
                for c in range(1, self.conditions + 1)]

    def _get_field_names_of_condition_operators(self) -> list:
        """
        Gets names for the condition operator fields
        depending on the number of `conditions`.

        :Example: ['cond_operator_1', 'cond_operator_2']
        """
        return ['cond_operator_{}'.format(c) for c in range(1, self.conditions + 1)]

    def _get_field_names_of_condition_constants(self) -> list:
        """
        Gets names for the condition constant fields
        depending on the number of `conditions`.

        :Example: ['cond_const_1', 'cond_const_2']
        """
        return ['cond_const_{}'.format(c) for c in range(1, self.conditions + 1)]

    def _get_field_names_of_conditions(self):
        """
        Gets names for the condition fields
        depending on the number of `variables` and `conditions`.

        :Example: ((['cond_coeff_1_1', 'cond_coeff_1_2'], 'cond_operator_1', 'cond_const_1'),
                   (['cond_coeff_2_1', 'cond_coeff_2_2'], 'cond_operator_2', 'cond_const_2'))
        """
        return zip(self._get_field_names_of_condition_coefficients(),
                   self._get_field_names_of_condition_operators(),
                   self._get_field_names_of_condition_constants())

    def _set_simplex_form_fields(self):
        for func_field_name in self._get_field_names_of_objective_function_coefficients():
            self.fields[func_field_name] = forms.FloatField()

        self.fields['tendency'] = forms.ChoiceField(
            initial='max', choices=[('max', 'max'), ('min', 'min')]
        )

        for cond_coeffs, operator_field_name, const_field_name in self._get_field_names_of_conditions():
            for cond_coeff_field_name in cond_coeffs:
                self.fields[cond_coeff_field_name] = forms.FloatField()
            self.fields[operator_field_name] = forms.ChoiceField(
                initial='<=',
                choices=[('<=', '<='), ('>=', '>='), ('=', '=')]
            )
            self.fields[const_field_name] = forms.FloatField()

    def solve(self):
        input_data = defaultdict(list)

        sign = 1 if self.cleaned_data['tendency'] == 'min' else -1
        input_data['c'] = [sign * self.cleaned_data[func_field_name]
                           for func_field_name in self._get_field_names_of_objective_function_coefficients()]

        for cond_coeffs, operator_field_name, const_field_name in self._get_field_names_of_conditions():
            operator = self.cleaned_data[operator_field_name]
            if operator == '<=' or operator == '>=':
                sign = 1 if operator == '<=' else -1
                input_data['b_ub'].append(sign * self.cleaned_data[const_field_name])
                input_data['A_ub'].append(
                    [sign * self.cleaned_data[cond_coeff_field_name] for cond_coeff_field_name in cond_coeffs]
                )
            else:
                input_data['b_eq'].append(self.cleaned_data[const_field_name])
                input_data['A_eq'].append(
                    [self.cleaned_data[cond_coeff_field_name] for cond_coeff_field_name in cond_coeffs]
                )

        result = linprog(**input_data)
        if self.cleaned_data['tendency'] == 'max':
            result['fun'] = -result['fun']

        return result
