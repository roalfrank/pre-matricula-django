
from django.views.generic import DetailView
from core.preMatricula.models import PreMatricula


class MatriculaDetailView(DetailView):
    model = PreMatricula
    template_name = "matricula/matricula/detalle_matricula.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context
