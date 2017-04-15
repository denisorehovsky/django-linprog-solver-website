from .base import WebTestBase


class TestSimplex(WebTestBase):

    def test_solve_linear_problem(self):
        self.get_url('simplex:init')
        self.fill({'#id_variables': '2',
                   '#id_conditions': '4',
                   '#id_is_non_negative': True})
        self.submit('button[type=submit]')

        self.assertRegex(self.current_url, '/simplex/solve/.+')
        self.assertIn('variables=2', self.current_url)
        self.assertIn('conditions=4', self.current_url)
        self.assertIn('is_non_negative=on', self.current_url)

        self.fill({'#id_func_coeff_1': '-12',
                   '#id_func_coeff_2': '5',
                   '#id_tendency': 'max',

                   '#id_cond_coeff_1_1': '0',
                   '#id_cond_coeff_1_2': '1',
                   '#id_cond_operator_1': '<=',
                   '#id_cond_const_1': '3',

                   '#id_cond_coeff_2_1': '3',
                   '#id_cond_coeff_2_2': '-5',
                   '#id_cond_operator_2': '<=',
                   '#id_cond_const_2': '0',

                   '#id_cond_coeff_3_1': '-2',
                   '#id_cond_coeff_3_2': '-1',
                   '#id_cond_operator_3': '<=',
                   '#id_cond_const_3': '-3',

                   '#id_cond_coeff_4_1': '-4',
                   '#id_cond_coeff_4_2': '1',
                   '#id_cond_operator_4': '<=',
                   '#id_cond_const_4': '4'})
        self.submit('button[type=submit]')

        self.assertRegex(self.current_url, '/simplex/results/')

        self.fail('Finish the test!')