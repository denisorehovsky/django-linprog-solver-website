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
