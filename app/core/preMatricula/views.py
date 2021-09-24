from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from .models import Estudiante, PreMatricula, PreMatriculaEstudiante

# Create your views here.


def esta_matriculado(user, id_matricula):
    matricula = PreMatricula.objects.filter(pk=id_matricula).first()
    matricula_estudiante = PreMatriculaEstudiante.objects.filter(
        estudiante__usuario=user, preMatricula=matricula).count()
    if matricula_estudiante >= 1:
        return True
    return False


@login_required
def getDetalle(request, id):
    template_name = "matricula/matricula/detalle_matricula_page.html"
    context = {}
    context['id_matricula'] = id
    return render(request, template_name, context)


class DetalleMatriculaPage(TemplateView):
    template_name = "matricula/matricula/detalle_matricula_page.html"
    id_matricula = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["id_matricula"] = int(self.request.GET.get('pk'))
        return context


@login_required
@permission_required('preMatricula.view_estudiante', raise_exception=True)
def buscarEstudiante(request):
    if request.method == 'POST':
        id_estudiante = int(request.POST['id_estudiante'])
        estudiante = Estudiante.objects.filter(pk=id_estudiante)[0]
        datos = estudiante.datosAllJson()
        datos['enviado'] = True
        return JsonResponse(datos, safe=False)
    return JsonResponse([], safe=False)


@login_required
@permission_required('preMatricula.view_estudiante', raise_exception=True)
def uniqueUser(request):
    if request.method == 'POST':
        try:
            # chequeamos si estamos en editar o add . si es editar hacemos la consulta con NONe
            # id_edit no se incluye en la consulta
            id_edit = request.POST['id_edit']
            if id_edit == "":
                id_edit = None
            # consulta a la base dato chequear el nombre usuario.
            user = User.objects.filter(
                ~Q(id=id_edit), username=request.POST['username'])
            if len(user) < 1:
                # si no hay resultado en la busqueda , se devuelve True, dando luz verde usuario.
                return JsonResponse(True, safe=False)
            # si hay resultado se retorna False para impedir que se cree  nombres repetidos.
            return JsonResponse(False, safe=False)
        except:
            return JsonResponse(False, safe=False)
