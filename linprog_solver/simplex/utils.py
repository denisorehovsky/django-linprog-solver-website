import sympy


def generate_latex_result(function_coefficients, tendency, constraints, solution):
    """
    Dummy code to generate latex result of solved linear programming problem.

    TODO: Find better solution.
    """
    variables = sympy.symbols('x1:{}'.format(str(len(function_coefficients) + 1)))

    F = sympy.symbols('F')
    function = sympy.Eq(F, sympy.Eq(
        sum(coeff * variable for coeff, variable in zip(function_coefficients, variables)),
        sympy.symbols('{}'.format(tendency))
    ))

    result = sympy.latex(function) + r'\\[0.3in]'

    inequalities = [sympy.Rel(sum(coeff * variable for coeff, variable in zip(coeffs, variables)), const, operator)
                    for coeffs, operator, const in constraints]
    for inequality in inequalities:
        result += r'\\' + sympy.latex(inequality)

    result += r'\\' + sympy.latex(sympy.Rel(sympy.symbols('X'), 0, '>='))

    result += r'\\[0.3in]' + sympy.latex(sympy.Eq(F, solution['fun']))

    for x_value in [sympy.Eq(variable, value) for variable, value in zip(variables, solution['x'])]:
        result += sympy.latex(r'\\') + sympy.latex(x_value)

    return result
