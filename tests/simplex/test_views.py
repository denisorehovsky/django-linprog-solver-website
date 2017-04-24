from test_plus.test import TestCase

from linprog_solver.simplex.forms import SimplexInitForm, SimplexSolveForm


class TestSimplexInitView(TestCase):

    def test_get(self):
        resp = self.get_check_200('simplex:init')
        self.assertTemplateUsed(resp, 'simplex/simplex_init.html')
        self.assertIsInstance(resp.context['form'], SimplexInitForm)


class TestSimplexSolveView(TestCase):

    def test_get(self):
        resp = self.get('simplex:solve', data={'variables': 2,
                                               'constraints': 4})
        self.response_200(resp)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertIsInstance(resp.context['form'], SimplexSolveForm)

    def test_post(self):
        resp = self.post('simplex:solve', data={
            'variables': 3, 'constraints': 4,

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
        self.response_200(resp)
        self.assertTemplateUsed(resp, 'simplex/simplex_result.html')
        self.assertIn('result', resp.context)
        self.assertIn('Optimization terminated successfully', resp.context['result'])

        resp = self.post('simplex:solve', data={
            'variables': '3', 'constraints': '4',

            'func_coeff_1': '4', 'func_coeff_2': '1', 'func_coeff_3': '-1', 'tendency': 'max',

            'constr_coeff_1_1': '2', 'constr_coeff_1_2': '-3', 'constr_coeff_1_3': '-2',
            'constr_operator_1': '>=', 'constr_const_1': '5',

            'constr_coeff_2_1': '-4', 'constr_coeff_2_2': '-1', 'constr_coeff_2_3': '2',
            'constr_operator_2': '>=', 'constr_const_2': '3',

            'constr_coeff_3_1': '3', 'constr_coeff_3_2': '-2', 'constr_coeff_3_3': '-4',
            'constr_operator_3': '>=', 'constr_const_3': '6',

            'constr_coeff_4_1': '1', 'constr_coeff_4_2': '1', 'constr_coeff_4_3': '1',
            'constr_operator_4': '<=', 'constr_const_4': '3'
        })
        self.response_200(resp)
        self.assertTemplateUsed(resp, 'simplex/simplex_result.html')
        self.assertIn('result', resp.context)
        self.assertIn('Problem appears to be infeasible', resp.context['result'])

    def test_post_with_bad_form_data(self):
        resp = self.post('simplex:solve', data={
            'variables': '1', 'constraints': '1',
            'func_coeff_1': '4', 'tendency': 'max',
            'constr_coeff_1_1': '5', 'constr_operator_1': '<=',
        })
        self.response_200(resp)
        self.assertEqual(len(resp.context['form'].errors), 1)

    def test_redirects_if_value_of_variables_and_constraints_are_invalid(self):
        resp = self.get('simplex:solve', data={'variables': 'should_be_num',
                                               'constraints': 4})
        self.response_302(resp)
        self.assertRedirects(resp, self.reverse('simplex:init'))

        resp = self.get('simplex:solve', data={'variables': 15,
                                               'constraints': 4})
        self.response_302(resp)
        self.assertRedirects(resp, self.reverse('simplex:init'))

        resp = self.post('simplex:solve', data={
            'variables': '15', 'constraints': '1',
            'func_coeff_1': '4', 'tendency': 'max',
            'constr_coeff_1_1': '5', 'constr_operator_1': '<=',
        })
        self.response_302(resp)
        self.assertRedirects(resp, self.reverse('simplex:init'))
