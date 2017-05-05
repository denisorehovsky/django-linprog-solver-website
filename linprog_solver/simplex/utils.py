import sympy

from .constants import STATUS


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
