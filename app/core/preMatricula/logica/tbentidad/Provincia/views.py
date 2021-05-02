from django.shortcuts import render
from django.views.generic import ListView
from core.preMatricula.models import Provincia

def createProvincia(request):
    data = {"title": "Listado Provincia",
            "icono_titulo": "fas fa-tachometer-alt",
            'body': [
                {'nombre': "Roaldys", "municipio": "Regla"},
                {'nombre': "Roaldys", "municipio": "Regla"},
                {'nombre': "Roaldys", "municipio": "Regla"},
                {'nombre': "Roaldys", "municipio": "Regla"},
                {'nombre': "Roaldys", "municipio": "Regla"}],
            'bodyEncabezado': [
                {'nombre': "Curso"},
                {'nombre': "Municipio"},
                {'nombre': "Accion"}
            ] }
    return render(request,"tbentidad/provincia/list.html",data)


class ProvinciaListView(ListView):
    model = Provincia
    template_name = "tbentidad/provincia/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Provincia"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        return context

