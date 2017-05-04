from django.conf import settings


def linprog_solver_processor(request):
    return {
        'LANGUAGES': getattr(settings, 'LANGUAGES', ''),
    }
