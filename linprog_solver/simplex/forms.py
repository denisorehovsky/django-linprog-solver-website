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
    constraints = forms.ChoiceField(
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
            Div(Field('constraints'), css_class='col-sm-3 col-md-2 text-center'),
            Div(css_class='clearfix'),
            Submit('submit', _('Next step'), css_class='col-md-offset-4'),
        )


class SimplexSolveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.variables, self.constraints = self._process_variables_and_constraints(
            kwargs.pop('variables', None), kwargs.pop('constraints', None)
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
                'Constraints',
                *[Div(*constr_coeffs, operator_field_name, const_field_name)
                  for constr_coeffs, operator_field_name, const_field_name in self._get_field_names_of_constraints()]
            ),
            HTML('<div style="margin-top:50px;"></div>'),
            Submit('submit', _('Next step')),
        )

    def _process_variables_and_constraints(self, variables: object, constraints: object) -> (int, int):
        try:
            variables, constraints = int(variables), int(constraints)
        except:
            raise SimplexInitException(_('Please define the number of variables and constraints'))

        if 1 <= variables <= 10 and 1 <= constraints <= 10:
            return variables, constraints
        else:
            raise SimplexInitException(_('The number of variables and constraints should be between 1 and 10'))

    def _get_field_names_of_objective_function_coefficients(self) -> list:
        """
        Gets names for the objective function coefficient fields
        depending on the number of `variables`.

        :Example: ['func_coeff_1', 'func_coeff_2', 'func_coeff_3']
        """
        return ['func_coeff_{}'.format(v) for v in range(1, self.variables + 1)]

    def _get_field_names_of_constraint_coefficients(self) -> list:
        """
        Gets names for the constraint coefficient fields
        depending on the number of `variables` and `constraints`.

        :Example: [['constr_coeff_1_1', 'constr_coeff_1_2'],
                   ['constr_coeff_2_1', 'constr_coeff_2_2']]
        """
        return [['constr_coeff_{}_{}'.format(c, v) for v in range(1, self.variables + 1)]
                for c in range(1, self.constraints + 1)]

    def _get_field_names_of_constraint_operators(self) -> list:
        """
        Gets names for the constraint operator fields
        depending on the number of `constraints`.

        :Example: ['constr_operator_1', 'constr_operator_2']
        """
        return ['constr_operator_{}'.format(c) for c in range(1, self.constraints + 1)]

    def _get_field_names_of_constraint_constants(self) -> list:
        """
        Gets names for the constraint constant fields
        depending on the number of `constraints`.

        :Example: ['constr_const_1', 'constr_const_2']
        """
        return ['constr_const_{}'.format(c) for c in range(1, self.constraints + 1)]

    def _get_field_names_of_constraints(self):
        """
        Gets names for the constraint fields
        depending on the number of `variables` and `constraints`.

        :Example: ((['constr_coeff_1_1', 'constr_coeff_1_2'], 'constr_operator_1', 'constr_const_1'),
                   (['constr_coeff_2_1', 'constr_coeff_2_2'], 'constr_operator_2', 'constr_const_2'))
        """
        return zip(self._get_field_names_of_constraint_coefficients(),
                   self._get_field_names_of_constraint_operators(),
                   self._get_field_names_of_constraint_constants())

    def _set_simplex_form_fields(self):
        for func_field_name in self._get_field_names_of_objective_function_coefficients():
            self.fields[func_field_name] = forms.FloatField()

        self.fields['tendency'] = forms.ChoiceField(
            initial='max', choices=[('max', 'max'), ('min', 'min')]
        )

        for constr_coeffs, operator_field_name, const_field_name in self._get_field_names_of_constraints():
            for constr_coeff_field_name in constr_coeffs:
                self.fields[constr_coeff_field_name] = forms.FloatField()
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

        for constr_coeffs, operator_field_name, const_field_name in self._get_field_names_of_constraints():
            operator = self.cleaned_data[operator_field_name]
            if operator == '<=' or operator == '>=':
                sign = 1 if operator == '<=' else -1
                input_data['b_ub'].append(sign * self.cleaned_data[const_field_name])
                input_data['A_ub'].append(
                    [sign * self.cleaned_data[constr_coeff_field_name] for constr_coeff_field_name in constr_coeffs]
                )
            else:
                input_data['b_eq'].append(self.cleaned_data[const_field_name])
                input_data['A_eq'].append(
                    [self.cleaned_data[constr_coeff_field_name] for constr_coeff_field_name in constr_coeffs]
                )

        result = linprog(**input_data)
        if self.cleaned_data['tendency'] == 'max':
            result['fun'] = -result['fun']

        return result
