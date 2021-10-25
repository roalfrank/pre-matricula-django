from django.contrib.auth.decorators import permission_required, login_required
import json
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from core.preMatricula.models import PreMatricula
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import PreMatriculaForm


class MatriculaDetailCargarFormAddView(TemplateView):
    template_name = "matricula/matricula_list/form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_matricula'] = PreMatriculaForm()
        return context


class MatriculaView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "matricula/matricula_list/matricula_list.html"
    permiso_vista = 'view_prematricula'
    permiso_crud = {
        'add': 'add_prematricula',
        'change': 'change_prematricula',
        'delete': 'delete_prematricula',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_matricula = PreMatriculaForm(request.POST)
                tipo = request.POST['tipo']
                if all([form_matricula.is_valid()]):
                    with transaction.atomic():
                        matricula = form_matricula.save()
                        data['enviado'] = True
                        data['nombre'] = matricula.curso.__str__()
                else:
                    data['enviado'] = False
                    data['error'] = form_matricula.errors.as_json()

            elif action == "cargarDatos":
                limite = int(request.POST['limite'])
                inicio = int(request.POST['inicio'])
                busqueda = request.POST['busqueda']
                if busqueda != '':
                    lista_filtro = {
                        'nombre': 'usuario__perfil__nombre__icontains',
                        'ci': 'usuario__perfil__ci__icontains',
                        'username': 'usuario__username__icontains',
                        'correo': 'usuario__perfil__correo__icontains',
                        'apellido1': 'usuario__perfil__apellido1__icontains',
                        'apellido2': 'usuario__perfil__apellido2__icontains',
                        'municipio': 'usuario__perfil__municipio__pk',
                        'provincia': 'usuario__perfil__municipio__provincia__pk',
                        'jcp': 'jcb__jcm__region__jcp__pk',
                        'region': 'jcb__jcm__region__pk',
                        'jcm': 'jcb__jcm__pk',
                        'jcb': 'jcb__pk',
                    }
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    for key, value in filtros.items():
                        condicion.add(
                            Q(**{lista_filtro[key]: value}), Q.AND)

                    matriculas = PreMatricula.objects.filter(condicion)
                else:
                    matriculas = PreMatricula.objects.filter(estado='AB')

                lista = [i.toJson()
                         for i in matriculas[inicio:inicio+limite]]
                data = {
                    'total': matriculas.count(),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                matricula = PreMatricula.objects.get(
                    pk=int(request.POST['id_edit']))
                form_matricula = PreMatriculaForm(
                    request.POST, instance=matricula)
                if all([form_matricula.is_valid()]):
                    with transaction.atomic():
                        matricula = form_matricula.save()
                        data['enviado'] = True
                        data['nombre'] = matricula.curso.__str__()
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_matricula.is_valid():
                        error.update(form_matricula.errors.get_json_data())
                    print(error)
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
                    delet_registro = PreMatricula.objects.filter(
                        pk__in=id_deletes)
                    for registro in delet_registro:
                        try:
                            registro.delete()
                        except Exception as e:
                            print('error borrar', e)
                            error.append(f"{registro.curso.__str__()}")
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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de curso a matricular"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_matricula'] = PreMatriculaForm()
        return context


@ login_required
@ permission_required('preMatricula.view_prematricula', raise_exception=True)
def buscarMatricula(request):
    if request.method == 'POST':
        id_matricula = int(request.POST['id_matricula'])
        matricula = PreMatricula.objects.filter(pk=id_matricula).first()
        datos = matricula.datosAllJson()
        datos['enviado'] = True
        return JsonResponse(datos, safe=False)
    return JsonResponse([], safe=False)
