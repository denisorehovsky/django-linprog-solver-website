from test_plus.test import TestCase

from linprog_solver.simplex.forms import SimplexInitForm, SimplexSolveForm


class TestSimplexInitView(TestCase):

    def test_returns_correct_status_code(self):
        self.get_check_200('simplex:init')

    def test_uses_correct_template(self):
        resp = self.get_check_200('simplex:init')
        self.assertTemplateUsed(resp, 'simplex/simplex_init.html')

    def test_context_data(self):
        resp = self.get_check_200('simplex:init')
        self.assertIsInstance(resp.context['form'], SimplexInitForm)


class TestSimplexSolveView(TestCase):

    def test_get(self):
        resp = self.get('simplex:solve', data={'variables': 2,
                                               'conditions': 4})
        self.response_200(resp)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertIsInstance(resp.context['form'], SimplexSolveForm)

    def test_get_with_incorrect_data_in_get_request(self):
        resp = self.get('simplex:solve', data={'variables': 'should_be_num',
                                               'conditions': 4})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertEqual(str(list(resp.context['messages'])[0]),
                         'Please define the number of variables and conditions')

        resp = self.get('simplex:solve', data={'variables': 15,
                                               'conditions': 4})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertEqual(str(list(resp.context['messages'])[0]),
                         'The number of variables and conditions should be between 1 and 10')

    def test_post(self):
        resp = self.post('simplex:solve', data={
            'variables': 3, 'conditions': 4,

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
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'simplex/simplex_result.html')
        self.assertIn('result', resp.context)

        resp = self.post('simplex:solve', data={
            'variables': '3', 'conditions': '4',

            'func_coeff_1': '4', 'func_coeff_2': '1', 'func_coeff_3': '-1', 'tendency': 'max',

            'cond_coeff_1_1': '2', 'cond_coeff_1_2': '-3', 'cond_coeff_1_3': '-2',
            'cond_operator_1': '>=', 'cond_const_1': '5',

            'cond_coeff_2_1': '-4', 'cond_coeff_2_2': '-1', 'cond_coeff_2_3': '2',
            'cond_operator_2': '>=', 'cond_const_2': '3',

            'cond_coeff_3_1': '3', 'cond_coeff_3_2': '-2', 'cond_coeff_3_3': '-4',
            'cond_operator_3': '>=', 'cond_const_3': '6',

            'cond_coeff_4_1': '1', 'cond_coeff_4_2': '1', 'cond_coeff_4_3': '1',
            'cond_operator_4': '<=', 'cond_const_4': '3'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertEqual(str(list(resp.context['messages'])[0]),
                         "The algorithm can't find an optimal solution.")

        def test_post_with_bad_form_data(self):
            resp = self.post('simplex:solve', data={
                'variables': '1', 'conditions': '1',
                'func_coeff_1': '4', 'tendency': 'max',
                'cond_coeff_1_1': '5', 'cond_operator_1': '<=',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'profiles/simplex_solve.html')
            self.assertEqual(len(resp.context['form'].errors), 1)
