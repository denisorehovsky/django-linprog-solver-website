from django.forms.fields import FloatField

from test_plus.test import TestCase

from linprog_solver.simplex.forms import (
    SimplexInitForm, SimplexCoefficientsForm
)


class TestSimplexInitForm(TestCase):

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

    def test_coefficient_float_fields(self):
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
