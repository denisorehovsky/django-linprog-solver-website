from typing import Any, Dict, Iterable

from django.utils.translation import ugettext_lazy as _

import sympy

from .constants import STATUS


class OptimizeSolution:

    def __init__(self):
        self.solution_steps = []

    def save_step(self, xk: Iterable[float], **kwargs: Dict[Any, Any]) -> None:
        """
        Saves step information to `solution_steps` before each iteration
        and after the final iteration of the simplex algorithm.

        :param xk: The current solution vector.
        :param tableau: The current tableau of the simplex algorithm.
        :param phase: The current Phase of the simplex algorithm (1 or 2).
        :param nit: The current iteration number.
        :param pivot: The index of the tableau selected as the next pivot,
                      or nan if no pivot exists.
        :param basis: A list of the current basic variables.
        :param complete: True if the simplex algorithm has completed
                         (and this is the final call to `save_step`),
                         otherwise False.
        :param status: The message that describes current iteration.
        """
        tableau = kwargs['tableau']  # type: Iterable[float]
        nit = kwargs['nit']  # type: int
        pivrow, pivcol = kwargs['pivot']  # type: int, int
        phase = kwargs['phase']  # type: int
        basis = kwargs['basis']  # type: Iterable[int]
        complete = kwargs['complete']  # type: bool

        if complete:
            status = _('Iteration Complete - Phase {0:d}').format(phase)
        elif nit == 0:
            status = _('Initial Tableau - Phase {0:d}').format(phase)
        else:
            status = _('Iteration {0:d} - Phase {1:d}').format(nit, phase)

        self.solution_steps.append({
            'xk': xk,
            'tableau': tableau,
            'nit': nit,
            'pivrow': pivrow,
            'pivcol': pivcol,
            'phase': phase,
            'basis': basis,
            'complete': complete,
            'status': status,
        })


def generate_latex_result(function_coefficients, tendency, constraints, result):
    """
    Dummy code that generates latex result of solved linear programming problem.

    TODO: Find better solution.
    """
    variables = sympy.symbols('x1:{}'.format(str(len(function_coefficients) + 1)))

    F = sympy.symbols('F')
    function = sympy.Eq(F, sympy.Eq(
        sum(coeff * variable for coeff, variable in zip(function_coefficients, variables)),
        sympy.symbols('{}'.format(tendency))
    ))

    latex = sympy.latex(function) + '\\\\[0.3in]'

    latex += '\\begin{cases}'
    inequalities = [sympy.Rel(sum(coeff * variable for coeff, variable in zip(coeffs, variables)), const, operator)
                    for coeffs, operator, const in constraints]
    for inequality in inequalities:
        latex += sympy.latex(inequality) + r'\\'
    latex += '\\end{cases}'

    latex += '\\\\' + sympy.latex(sympy.Rel(sympy.symbols('X'), 0, '>='))

    latex += '\\\\[0.3in] \\text{%s}' % STATUS[result['status']]

    if result['success']:
        latex += '\\\\[0.2in]' + sympy.latex(sympy.Eq(F, result['fun']))

        for x_value in [sympy.Eq(variable, value) for variable, value in zip(variables, result['x'])]:
            latex += sympy.latex(r'\\') + sympy.latex(x_value)

    return latex
