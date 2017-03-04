from .base import WebTestBase


class TestSimplex(WebTestBase):

    def test_solve_linear_problem(self):
        self.get_url('simplex:init')
        self.fill({'#id_variables': '2',
                   '#id_conditions': '4'})
        self.submit('button[type=submit]')

        self.assertRegex(self.current_url, '/simplex/solve/.+')
        self.assertIn('variables=2', self.current_url)
        self.assertIn('conditions=4', self.current_url)
        self.assertIn('is_non_negative=on', self.current_url)

        self.fail('Finish the test!')
