from django import template


register = template.Library()


@register.inclusion_tag('simplex/_solution_steps.html')
def show_solution_steps(solution_steps):
    return {
        'solution_steps': solution_steps,
    }
