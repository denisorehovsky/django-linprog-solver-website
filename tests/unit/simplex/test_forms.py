from test_plus.test import TestCase

from linprog_solver.simplex.forms import SimplexInitForm


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
