from .base import WebTestBase, SeleniumTestBase


class SimplexSeleniumTests(SeleniumTestBase):

    def test_solve_linear_problem(self):
        self.get_url('simplex:init')
        self.fill({'#id_variables': '2',
                   '#id_constraints': '4'})
        self.submit('input[type=submit]')

        self.assertRegex(self.current_url, '/simplex/solve/.+')
        self.assertIn('variables=2', self.current_url)
        self.assertIn('constraints=4', self.current_url)

        self.fill({'#id_func_coeff_1': '-12',
                   '#id_func_coeff_2': '5',
                   '#id_tendency': 'max',

                   '#id_constr_coeff_1_1': '0',
                   '#id_constr_coeff_1_2': '1',
                   '#id_constr_operator_1': '<=',
                   '#id_constr_const_1': '3',

                   '#id_constr_coeff_2_1': '3',
                   '#id_constr_coeff_2_2': '-5',
                   '#id_constr_operator_2': '<=',
                   '#id_constr_const_2': '0',

                   '#id_constr_coeff_3_1': '-2',
                   '#id_constr_coeff_3_2': '-1',
                   '#id_constr_operator_3': '<=',
                   '#id_constr_const_3': '-3',

                   '#id_constr_coeff_4_1': '-4',
                   '#id_constr_coeff_4_2': '1',
                   '#id_constr_operator_4': '<=',
                   '#id_constr_const_4': '4'})
        self.submit('input[type=submit]')

        self.assertRegex(self.current_url, '/simplex/solve/')
        self.assertTextPresent('Result')

        self.fail('Finish the test!')


class SimplexWebTests(WebTestBase):

    def test_solve_with_incorrect_get_request_data(self):
        self.get_literal_url('/simplex/solve/?variables=15&constraints=3')
        self.assertUrlsEqual(self.current_url, '/simplex/')
        self.assertTextPresent('The number of variables and constraints should be between 1 and 10')

        self.get_literal_url('/simplex/solve/?variables=number&constraints=5')
        self.assertUrlsEqual(self.current_url, '/simplex/')
        self.assertTextPresent('Please define the number of variables and constraints')
