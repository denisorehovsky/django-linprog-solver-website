from .base import WebTestBase


class TestSimplex(WebTestBase):

    def test_solve_linear_problem(self):
        self.get_url('simplex:init')
        self.fill({'#id_coefficients_number': '2',
                   '#id_constraints_number': '4'})
        self.submit('button[type=submit]')

        self.assertRegex(self.current_url, '/simplex/solve/.+')
        self.assertIn('coefficients_number=2', self.current_url)
        self.assertIn('constraints_number=4', self.current_url)
        self.assertIn('is_non_negative=on', self.current_url)

        self.fail('Finish the test!')
