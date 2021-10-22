import json
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from core.preMatricula.models import Curso
from core.user.models import Perfil
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import CursoForm


class CursoDetailCargarFormAddView(TemplateView):
    template_name = "curso/curso/form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_curso'] = CursoForm()
        return context


class CursoDetailView(DetailView):
    model = Curso
    template_name = "curso/curso/detailCurso.html"

    def get_context_data(self, **kwargs):
        print(self.request.GET.get('next'))
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


class CursoView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "curso/curso/curso_list.html"
    permiso_vista = 'view_curso'
    permiso_crud = {
        'add': 'add_curso',
        'change': 'change_curso',
        'delete': 'delete_curso',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_curso = CursoForm(request.POST, request.FILES)
                if all([form_curso.is_valid()]):
                    with transaction.atomic():
                        curso = form_curso.save()
                        data['enviado'] = True
                        data['nombre'] = curso.nombre
                else:
                    data['enviado'] = False
                    data['error'] = form_curso.errors.as_json()

            elif action == "cargarDatos":
                print(request.POST)
                limite = int(request.POST['limite'])
                inicio = int(request.POST['inicio'])
                busqueda = request.POST['busqueda']
                if busqueda != '':
                    lista_filtro = {
                        'nombre': 'nombre__icontains',
                        'duracion': 'duracion__icontains',
                        'corto': 'corto__icontains',
                    }
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    for key, value in filtros.items():
                        condicion.add(Q(**{lista_filtro[key]: value}), Q.AND)

                    cursos = Curso.objects.filter(condicion)
                else:
                    cursos = Curso.objects.all()
                    print('cursos', cursos)

                lista = [i.toJson()
                         for i in cursos[inicio:inicio+limite]]
                data = {
                    'total': cursos.count(),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una curso.
            elif action == 'edit':
                curso = Curso.objects.get(
                    pk=int(request.POST['id_edit']))
                form_curso = CursoForm(
                    request.POST, instance=curso)
                if all([form_curso.is_valid()]):
                    with transaction.atomic():
                        curso = form_curso.save()
                        data['enviado'] = True
                        data['nombre'] = curso.nombre
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_curso.is_valid():
                        print('error formulario curso')
                        error.update(form_curso.errors.get_json_data())
                    data['error'] = json.dumps(error)

            # action delete, eliminar una registro
            elif action == "delete":
                try:
                    id_deletes = []
                    error = []
                    id = json.loads(request.POST["id"])
                    if type(id) == int:
                        id_deletes.append(id)
                    else:
                        id_deletes.extend(id)
                    delet_registro = Curso.objects.filter(
                        pk__in=id_deletes)
                    for registro in delet_registro:
                        try:
                            registro.delete()
                        except Exception as e:
                            error.append(f"{registro.username}")
                    if len(error) > 0:
                        data['error'] = error
                except Exception as e:
                    if type(e) == RestrictedError:
                        data['error'] = "Esta estado tiene registro vinculados, no se puede borrar."
                    else:
                        print(type(e))
                        data['error'] = e
        except Exception as e:
            # comprobar los errores , esto despues solo dejar a data['error']
            print(e)
            print(e.args)
            print(type(e))
            print('type(e) ver si es aqui')
            data['enviado'] = False
            data['error'] = 'Error en las operaciones con los registros'
        print(data)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Cursos"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_curso'] = CursoForm()
        return context


@ login_required
@ permission_required('preMatricula.view_curso', raise_exception=True)
def buscarCurso(request):
    if request.method == 'POST':
        id_curso = int(request.POST['id_curso'])
        curso = Curso.objects.filter(pk=id_curso).first()
        return JsonResponse(curso.toJson(), safe=False)
    return JsonResponse([], safe=False)
