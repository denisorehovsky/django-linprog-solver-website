from django.forms.fields import FloatField

from test_plus.test import TestCase

from linprog_solver.simplex.exceptions import SimplexInitException
from linprog_solver.simplex.forms import (
    SimplexInitForm, SimplexSolveForm
)


class TestSimplexInitForm(TestCase):

    def test_save_form(self):
        form = SimplexInitForm(data={
            'variables': '2',
            'conditions': '4',
        })
        self.assertTrue(form.is_valid())

    def test_errors(self):
        form = SimplexInitForm(data={
            'variables': '15',
            'conditions': '4'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_variables_choice_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['variables'].initial, 3)
        self.assertEqual(
            form.fields['variables'].choices,
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
             (8, 8), (9, 9), (10, 10)]
        )

    def test_conditions_choice_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['conditions'].initial, 3)
        self.assertEqual(
            form.fields['conditions'].choices,
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
             (8, 8), (9, 9), (10, 10)]
        )


class TestSimplexSolveForm(TestCase):

    def test_save_form(self):
        form = SimplexSolveForm(variables=2, conditions=3, data={
            'func_coeff_1': '5', 'func_coeff_2': '2.5', 'tendency': 'max',
            'cond_coeff_1_1': '2', 'cond_coeff_1_2': '1', 'cond_operator_1': '<=', 'cond_const_1': '5',
            'cond_coeff_2_1': '3.5', 'cond_coeff_2_2': '0', 'cond_operator_2': '>=', 'cond_const_2': '1',
            'cond_coeff_3_1': '2', 'cond_coeff_3_2': '2', 'cond_operator_3': '=', 'cond_const_3': '3',
        })
        self.assertTrue(form.is_valid())

    def test_errors(self):
        form = SimplexSolveForm(variables=2, conditions=3, data={
            'func_coeff_1': '5', 'func_coeff_2': '2.5', 'tendency': 'max',
            'cond_coeff_1_1': '2', 'cond_coeff_1_2': '1', 'cond_operator_1': '<=', 'cond_const_1': '5',
            'cond_coeff_2_1': '3.5', 'cond_coeff_2_2': '0', 'cond_operator_2': '>=', 'cond_const_2': '1',
            'cond_coeff_3_1': '2', 'cond_coeff_3_2': 'number', 'cond_operator_3': '=',
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors), 2)

    def test_process_variables_and_conditions(self):
        SimplexSolveForm(variables=2, conditions=3)

        with self.assertRaises(SimplexInitException) as error:
            SimplexSolveForm()
        self.assertEqual(str(error.exception), 'Please define the number of variables and conditions')

        with self.assertRaises(SimplexInitException) as error:
            SimplexSolveForm(variables=2, conditions='should_be_a_number')
        self.assertEqual(str(error.exception), 'Please define the number of variables and conditions')

        with self.assertRaises(SimplexInitException) as error:
            SimplexSolveForm(variables=5, conditions='11')
        self.assertEqual(str(error.exception), 'The number of variables and conditions should be between 1 and 10')

    def test_get_field_names_of_objective_function_coefficients(self):
        variables, conditions = 2, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        self.assertEqual(form._get_field_names_of_objective_function_coefficients(),
                         ['func_coeff_1', 'func_coeff_2'])

    def test_get_field_names_of_condition_coefficients(self):
        variables, conditions = 2, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        self.assertEqual(
            form._get_field_names_of_condition_coefficients(),
            [['cond_coeff_1_1', 'cond_coeff_1_2'],
             ['cond_coeff_2_1', 'cond_coeff_2_2'],
             ['cond_coeff_3_1', 'cond_coeff_3_2']]
        )

    def test_get_field_names_of_condition_operators(self):
        variables, conditions = 2, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        self.assertEqual(form._get_field_names_of_condition_operators(),
                         ['cond_operator_1', 'cond_operator_2', 'cond_operator_3'])

    def test_get_field_names_of_condition_constants(self):
        variables, conditions = 2, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        self.assertEqual(form._get_field_names_of_condition_constants(),
                         ['cond_const_1', 'cond_const_2', 'cond_const_3'])

    def test_get_field_names_of_conditions(self):
        variables, conditions = 2, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        self.assertEqual(
            list(form._get_field_names_of_conditions()),
            [(['cond_coeff_1_1', 'cond_coeff_1_2'], 'cond_operator_1', 'cond_const_1'),
             (['cond_coeff_2_1', 'cond_coeff_2_2'], 'cond_operator_2', 'cond_const_2'),
             (['cond_coeff_3_1', 'cond_coeff_3_2'], 'cond_operator_3', 'cond_const_3')]
        )

    def test_func_coeff_float_fields(self):
        variables, conditions = 4, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        for i in range(1, variables + 1):
            key = 'func_coeff_{}'.format(i)
            self.assertIsInstance(form.fields[key], FloatField)

    def test_tendency_choice_field(self):
        form = SimplexSolveForm(variables=4, conditions=3)
        self.assertEqual(form.fields['tendency'].initial, 'max')
        self.assertEqual(
            form.fields['tendency'].choices,
            [('max', 'max'), ('min', 'min')]
        )

    def test_cond_coeff_float_field(self):
        variables, conditions = 4, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        for i in range(1, conditions + 1):
            for k in range(1, variables + 1):
                key = 'cond_coeff_{}_{}'.format(i, k)
                self.assertIsInstance(form.fields[key], FloatField)

    def test_cond_operator_field(self):
        form = SimplexSolveForm(variables=4, conditions=1)
        self.assertEqual(form.fields['cond_operator_1'].initial, '<=')
        self.assertEqual(
            form.fields['cond_operator_1'].choices,
            [('<=', '<='), ('>=', '>='), ('=', '=')]
        )

    def test_cond_const_float_field(self):
        variables, conditions = 4, 3
        form = SimplexSolveForm(variables=variables, conditions=conditions)
        for i in range(1, conditions + 1):
            key = 'cond_const_{}'.format(i)
            self.assertIsInstance(form.fields[key], FloatField)

    def test_solve(self):
        form = SimplexSolveForm(variables=3, conditions=4, data={
            'func_coeff_1': '300', 'func_coeff_2': '250', 'func_coeff_3': '450', 'tendency': 'max',

            'cond_coeff_1_1': '15', 'cond_coeff_1_2': '20', 'cond_coeff_1_3': '25',
            'cond_operator_1': '<=', 'cond_const_1': '1200',

            'cond_coeff_2_1': '35', 'cond_coeff_2_2': '60', 'cond_coeff_2_3': '60',
            'cond_operator_2': '<=', 'cond_const_2': '3000',

            'cond_coeff_3_1': '20', 'cond_coeff_3_2': '30', 'cond_coeff_3_3': '25',
            'cond_operator_3': '<=', 'cond_const_3': '1500',

            'cond_coeff_4_1': '0', 'cond_coeff_4_2': '250', 'cond_coeff_4_3': '0',
            'cond_operator_4': '>=', 'cond_const_4': '500'
        })
        self.assertTrue(form.is_valid())
        result = form.solve()
        self.assertTrue(result['fun'], 23060.0)
        self.assertTrue(list(result['x']), [56.0, 2, 12.8])

        form = SimplexSolveForm(variables=3, conditions=3, data={
            'func_coeff_1': '2', 'func_coeff_2': '1', 'func_coeff_3': '1', 'func_coeff_4': '4',
            'tendency': 'min',

            'cond_coeff_1_1': '1', 'cond_coeff_1_2': '-1', 'cond_coeff_1_3': '2', 'cond_coeff_1_4': '-1',
            'cond_operator_1': '>=', 'cond_const_1': '4',

            'cond_coeff_2_1': '2', 'cond_coeff_2_2': '1', 'cond_coeff_2_3': '-1', 'cond_coeff_2_4': '0',
            'cond_operator_2': '<=', 'cond_const_2': '8',

            'cond_coeff_3_1': '1', 'cond_coeff_3_2': '-1', 'cond_coeff_3_3': '-1', 'cond_coeff_3_4': '3',
            'cond_operator_3': '=', 'cond_const_3': '3',
        })
        self.assertTrue(form.is_valid())
        result = form.solve()
        self.assertTrue(result['fun'], 7.0)
        self.assertTrue(list(result['x']), [10 / 3, 0, 1 / 3])
