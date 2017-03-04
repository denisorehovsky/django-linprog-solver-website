from django.forms.fields import FloatField

from test_plus.test import TestCase

from linprog_solver.simplex.forms import (
    SimplexInitForm, SimplexCoefficientsForm
)


class TestSimplexInitForm(TestCase):

    def test_coefficients_number_choice_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['coefficients_number'].initial, 3)
        self.assertEqual(
            form.fields['coefficients_number'].choices,
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
             (8, 8), (9, 9), (10, 10)]
        )

    def test_constraints_number_choice_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['constraints_number'].initial, 3)
        self.assertEqual(
            form.fields['constraints_number'].choices,
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
             (8, 8), (9, 9), (10, 10)]
        )

    def test_is_non_negative_boolean_field(self):
        form = SimplexInitForm()
        self.assertEqual(form.fields['is_non_negative'].initial, True)
        self.assertEqual(form.fields['is_non_negative'].required, False)


class TestSimplexCoefficientsForm(TestCase):

    def test_coefficient_float_fields(self):
        form = SimplexCoefficientsForm(coefficients_number=4)
        for i in range(1, 5):
            key = 'coefficient_{}'.format(i)
            self.assertIsInstance(form.fields[key], FloatField)

    def test_tendency_choice_field(self):
        form = SimplexCoefficientsForm(coefficients_number=4)
        self.assertEqual(form.fields['tendency'].initial, 'max')
        self.assertEqual(
            form.fields['tendency'].choices,
            [('max', 'max'), ('min', 'min')]
        )
