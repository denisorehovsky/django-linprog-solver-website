from django.views.generic import TemplateView, FormView

from .forms import SimplexInitForm


class SimplexInitView(FormView):
    template_name = 'simplex/simplex_init.html'
    form_class = SimplexInitForm


class SimplexSolveView(TemplateView):
    template_name = 'simplex/simplex_solve.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
