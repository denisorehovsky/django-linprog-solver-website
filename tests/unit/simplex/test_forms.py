from django.forms.fields import FloatField

from test_plus.test import TestCase

from linprog_solver.simplex.forms import (
    SimplexInitForm, SimplexCoefficientsForm
)


class TestSimplexInitForm(TestCase):

    def test_save_form(self):
        form = SimplexInitForm(data={
            'variables': '2',
            'conditions': '4',
            'is_non_negative': False,
        })
        self.assertTrue(form.is_valid())

    def test_errors(self):
        form = SimplexInitForm(data={
            'tendency': 'max',
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

    def test_is_non_negative_boolean_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['is_non_negative'].initial, True)
        self.assertEqual(form.fields['is_non_negative'].required, False)


class TestSimplexCoefficientsForm(TestCase):

    def test_save_form(self):
        form = SimplexCoefficientsForm(variables=4, data={
            'tendency': 'max',
            'variable_1': '2',
            'variable_2': '2.5',
            'variable_3': '5',
            'variable_4': '1',
        })
        self.assertTrue(form.is_valid())

    def test_errors(self):
        form = SimplexCoefficientsForm(variables=3, data={
            'tendency': 'max',
            'variable_1': '2',
            'variable_2': 'number',
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors), 2)

    def test_variable_float_fields(self):
        form = SimplexCoefficientsForm(variables=4)
        for i in range(1, 5):
            key = 'variable_{}'.format(i)
            self.assertIsInstance(form.fields[key], FloatField)

    def test_tendency_choice_field(self):
        form = SimplexCoefficientsForm(variables=4)
        self.assertEqual(form.fields['tendency'].initial, 'max')
        self.assertEqual(
            form.fields['tendency'].choices,
            [('max', 'max'), ('min', 'min')]
        )
