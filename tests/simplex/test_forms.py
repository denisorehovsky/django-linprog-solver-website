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
            'constraints': '4',
        })
        self.assertTrue(form.is_valid())

    def test_errors(self):
        form = SimplexInitForm(data={
            'variables': '15',
            'constraints': '4'
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

    def test_constraints_choice_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['constraints'].initial, 3)
        self.assertEqual(
            form.fields['constraints'].choices,
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
             (8, 8), (9, 9), (10, 10)]
        )


class TestSimplexSolveForm(TestCase):

    def test_save_form(self):
        form = SimplexSolveForm(variables=2, constraints=3, data={
            'func_coeff_1': '5', 'func_coeff_2': '2.5', 'tendency': 'max',
            'constr_coeff_1_1': '2', 'constr_coeff_1_2': '1', 'constr_operator_1': '<=', 'constr_const_1': '5',
            'constr_coeff_2_1': '3.5', 'constr_coeff_2_2': '0', 'constr_operator_2': '>=', 'constr_const_2': '1',
            'constr_coeff_3_1': '2', 'constr_coeff_3_2': '2', 'constr_operator_3': '=', 'constr_const_3': '3',
        })
        self.assertTrue(form.is_valid())

    def test_errors(self):
        form = SimplexSolveForm(variables=2, constraints=3, data={
            'func_coeff_1': '5', 'func_coeff_2': '2.5', 'tendency': 'max',
            'constr_coeff_1_1': '2', 'constr_coeff_1_2': '1', 'constr_operator_1': '<=', 'constr_const_1': '5',
            'constr_coeff_2_1': '3.5', 'constr_coeff_2_2': '0', 'constr_operator_2': '>=', 'constr_const_2': '1',
            'constr_coeff_3_1': '2', 'constr_coeff_3_2': 'number', 'constr_operator_3': '=',
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors), 2)

    def test_process_variables_and_constraints(self):
        SimplexSolveForm(variables=2, constraints=3)

        with self.assertRaises(SimplexInitException) as error:
            SimplexSolveForm()
        self.assertEqual(str(error.exception), 'Please define the number of variables and constraints')

        with self.assertRaises(SimplexInitException) as error:
            SimplexSolveForm(variables=2, constraints='should_be_a_number')
        self.assertEqual(str(error.exception), 'Please define the number of variables and constraints')

        with self.assertRaises(SimplexInitException) as error:
            SimplexSolveForm(variables=5, constraints='11')
        self.assertEqual(str(error.exception), 'The number of variables and constraints should be between 1 and 10')

    def test_get_field_names_of_objective_function_coefficients(self):
        variables, constraints = 2, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        self.assertEqual(form._get_field_names_of_objective_function_coefficients(),
                         ['func_coeff_1', 'func_coeff_2'])

    def test_get_field_names_of_constraint_coefficients(self):
        variables, constraints = 2, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        self.assertEqual(
            form._get_field_names_of_constraint_coefficients(),
            [['constr_coeff_1_1', 'constr_coeff_1_2'],
             ['constr_coeff_2_1', 'constr_coeff_2_2'],
             ['constr_coeff_3_1', 'constr_coeff_3_2']]
        )

    def test_get_field_names_of_constraint_operators(self):
        variables, constraints = 2, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        self.assertEqual(form._get_field_names_of_constraint_operators(),
                         ['constr_operator_1', 'constr_operator_2', 'constr_operator_3'])

    def test_get_field_names_of_constraint_constants(self):
        variables, constraints = 2, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        self.assertEqual(form._get_field_names_of_constraint_constants(),
                         ['constr_const_1', 'constr_const_2', 'constr_const_3'])

    def test_get_field_names_of_constraints(self):
        variables, constraints = 2, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        self.assertEqual(
            list(form._get_field_names_of_constraints()),
            [(['constr_coeff_1_1', 'constr_coeff_1_2'], 'constr_operator_1', 'constr_const_1'),
             (['constr_coeff_2_1', 'constr_coeff_2_2'], 'constr_operator_2', 'constr_const_2'),
             (['constr_coeff_3_1', 'constr_coeff_3_2'], 'constr_operator_3', 'constr_const_3')]
        )

    def test_func_coeff_float_fields(self):
        variables, constraints = 4, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        for i in range(1, variables + 1):
            key = 'func_coeff_{}'.format(i)
            self.assertIsInstance(form.fields[key], FloatField)

    def test_tendency_choice_field(self):
        form = SimplexSolveForm(variables=4, constraints=3)
        self.assertEqual(form.fields['tendency'].initial, 'max')
        self.assertEqual(
            form.fields['tendency'].choices,
            [('max', 'max'), ('min', 'min')]
        )

    def test_constr_coeff_float_field(self):
        variables, constraints = 4, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        for i in range(1, constraints + 1):
            for k in range(1, variables + 1):
                key = 'constr_coeff_{}_{}'.format(i, k)
                self.assertIsInstance(form.fields[key], FloatField)

    def test_constr_operator_field(self):
        form = SimplexSolveForm(variables=4, constraints=1)
        self.assertEqual(form.fields['constr_operator_1'].initial, '<=')
        self.assertEqual(
            form.fields['constr_operator_1'].choices,
            [('<=', '<='), ('>=', '>='), ('=', '=')]
        )

    def test_constr_const_float_field(self):
        variables, constraints = 4, 3
        form = SimplexSolveForm(variables=variables, constraints=constraints)
        for i in range(1, constraints + 1):
            key = 'constr_const_{}'.format(i)
            self.assertIsInstance(form.fields[key], FloatField)

    def test_solve(self):
        form = SimplexSolveForm(variables=3, constraints=4, data={
            'func_coeff_1': '300', 'func_coeff_2': '250', 'func_coeff_3': '450', 'tendency': 'max',

            'constr_coeff_1_1': '15', 'constr_coeff_1_2': '20', 'constr_coeff_1_3': '25',
            'constr_operator_1': '<=', 'constr_const_1': '1200',

            'constr_coeff_2_1': '35', 'constr_coeff_2_2': '60', 'constr_coeff_2_3': '60',
            'constr_operator_2': '<=', 'constr_const_2': '3000',

            'constr_coeff_3_1': '20', 'constr_coeff_3_2': '30', 'constr_coeff_3_3': '25',
            'constr_operator_3': '<=', 'constr_const_3': '1500',

            'constr_coeff_4_1': '0', 'constr_coeff_4_2': '250', 'constr_coeff_4_3': '0',
            'constr_operator_4': '>=', 'constr_const_4': '500'
        })
        self.assertTrue(form.is_valid())
        result = form.solve()
        self.assertTrue(result['fun'], 23060.0)
        self.assertTrue(list(result['x']), [56.0, 2, 12.8])

        form = SimplexSolveForm(variables=3, constraints=3, data={
            'func_coeff_1': '2', 'func_coeff_2': '1', 'func_coeff_3': '1', 'func_coeff_4': '4',
            'tendency': 'min',

            'constr_coeff_1_1': '1', 'constr_coeff_1_2': '-1', 'constr_coeff_1_3': '2', 'constr_coeff_1_4': '-1',
            'constr_operator_1': '>=', 'constr_const_1': '4',

            'constr_coeff_2_1': '2', 'constr_coeff_2_2': '1', 'constr_coeff_2_3': '-1', 'constr_coeff_2_4': '0',
            'constr_operator_2': '<=', 'constr_const_2': '8',

            'constr_coeff_3_1': '1', 'constr_coeff_3_2': '-1', 'constr_coeff_3_3': '-1', 'constr_coeff_3_4': '3',
            'constr_operator_3': '=', 'constr_const_3': '3',
        })
        self.assertTrue(form.is_valid())
        result = form.solve()
        self.assertTrue(result['fun'], 7.0)
        self.assertTrue(list(result['x']), [10 / 3, 0, 1 / 3])
