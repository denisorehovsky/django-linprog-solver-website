from django.views.generic import TemplateView

from .forms import SimplexInitForm


class SimplexInitView(TemplateView):
    template_name = 'simplex/simplex_init.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = SimplexInitForm()
        return self.render_to_response(context)


class SimplexSolveView(TemplateView):
    template_name = 'simplex/simplex_solve.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
