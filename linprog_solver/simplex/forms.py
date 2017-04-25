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
                *[Div(HTML('<strong>CS{}</strong>'.format(i + 1)),
                      *constr_coeffs, operator_field_name, const_field_name,
                      HTML('<div style="margin-top:20px;"></div>'))
                  for i, (constr_coeffs,
                          operator_field_name,
                          const_field_name) in enumerate(self._get_field_names_of_constraints())]
            ),
            HTML('<div style="margin-top:50px;"></div>'),
            Submit('submit', _('Solve')),
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

    def _set_simplex_form_fields(self):
        for x, func_field_name in enumerate(self._get_field_names_of_objective_function_coefficients()):
            self.fields[func_field_name] = forms.FloatField(label='X{}'.format(x + 1))

        self.fields['tendency'] = forms.ChoiceField(
            initial='max', choices=[('max', 'max'), ('min', 'min')]
        )

        for constr_coeffs, operator_field_name, const_field_name in self._get_field_names_of_constraints():
            for x, constr_coeff_field_name in enumerate(constr_coeffs):
                self.fields[constr_coeff_field_name] = forms.FloatField(label='X{}'.format(x + 1))
            self.fields[operator_field_name] = forms.ChoiceField(
                initial='<=',
                choices=[('<=', '<='), ('>=', '>='), ('==', '==')]
            )
            self.fields[const_field_name] = forms.FloatField(label='')

    def _get_field_names_of_objective_function_coefficients(self) -> list:
        """
        Gets names for the objective function coefficient fields
        depending on the number of `variables`.

        :Example: ['func_coeff_1', 'func_coeff_2', 'func_coeff_3']
        """
        return ['func_coeff_{}'.format(v) for v in range(1, self.variables + 1)]

    def get_values_of_objective_function_coefficients(self) -> list:
        """
        Gets values of objective function coefficients.

        :Example: [2, 5, 1]
        """
        return [self.cleaned_data[coeff_field_name]
                for coeff_field_name in self._get_field_names_of_objective_function_coefficients()]

    def _get_field_names_of_constraint_coefficients(self) -> list:
        """
        Gets names for the constraint coefficient fields
        depending on the number of `variables` and `constraints`.

        :Example: [['constr_coeff_1_1', 'constr_coeff_1_2'],
                   ['constr_coeff_2_1', 'constr_coeff_2_2']]
        """
        return [['constr_coeff_{}_{}'.format(c, v) for v in range(1, self.variables + 1)]
                for c in range(1, self.constraints + 1)]

    def get_values_of_constraint_coefficients(self) -> list:
        """
        Gets values of constraint coefficients.

        :Example: [[1, 2.5],
                   [2, 5.1]]
        """
        return [[self.cleaned_data[coeff_field_name] for coeff_field_name in coefficients]
                for coefficients in self._get_field_names_of_constraint_coefficients()]

    def _get_field_names_of_constraint_operators(self) -> list:
        """
        Gets names for the constraint operator fields
        depending on the number of `constraints`.

        :Example: ['constr_operator_1', 'constr_operator_2']
        """
        return ['constr_operator_{}'.format(c) for c in range(1, self.constraints + 1)]

    def get_values_of_constraint_operators(self) -> list:
        """
        Gets values of constraint operators.

        :Example: ['<=', '=']
        """
        return [self.cleaned_data[operator_field_name]
                for operator_field_name in self._get_field_names_of_constraint_operators()]

    def _get_field_names_of_constraint_constants(self) -> list:
        """
        Gets names for the constraint constant fields
        depending on the number of `constraints`.

        :Example: ['constr_const_1', 'constr_const_2']
        """
        return ['constr_const_{}'.format(c) for c in range(1, self.constraints + 1)]

    def get_values_of_constraint_constants(self) -> list:
        """
        Gets values of constraint constants.

        :Example: [25, 60]
        """
        return [self.cleaned_data[const_field_name]
                for const_field_name in self._get_field_names_of_constraint_constants()]

    def _get_field_names_of_constraints(self):
        """
        Gets names for the constraint fields.

        :Example: ((['constr_coeff_1_1', 'constr_coeff_1_2'], 'constr_operator_1', 'constr_const_1'),
                   (['constr_coeff_2_1', 'constr_coeff_2_2'], 'constr_operator_2', 'constr_const_2'))
        """
        return zip(self._get_field_names_of_constraint_coefficients(),
                   self._get_field_names_of_constraint_operators(),
                   self._get_field_names_of_constraint_constants())

    def get_values_of_constraints(self):
        """
        Gets values of constraints.

        :Example: (([1, 2.5], '<=', '25'),
                   ([2, 5.1], '==', '60'))
        """
        return zip(self.get_values_of_constraint_coefficients(),
                   self.get_values_of_constraint_operators(),
                   self.get_values_of_constraint_constants())

    def solve(self):
        input_data = defaultdict(list)

        sign = 1 if self.cleaned_data['tendency'] == 'min' else -1
        input_data['c'] = [sign * func_coeff
                           for func_coeff in self.get_values_of_objective_function_coefficients()]

        for constr_coeffs, operator, const in self.get_values_of_constraints():
            if operator == '<=' or operator == '>=':
                sign = 1 if operator == '<=' else -1
                input_data['b_ub'].append(sign * const)
                input_data['A_ub'].append(
                    [sign * coefficient for coefficient in constr_coeffs]
                )
            else:
                input_data['b_eq'].append(const)
                input_data['A_eq'].append(constr_coeffs)

        result = linprog(**input_data)
        if self.cleaned_data['tendency'] == 'max':
            result['fun'] = -result['fun']

        return result
